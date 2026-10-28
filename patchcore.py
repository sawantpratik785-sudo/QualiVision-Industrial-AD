import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from sklearn.random_projection import SparseRandomProjection
from sklearn.metrics import roc_auc_score
from scipy.ndimage import gaussian_filter

class PatchCore(nn.Module):
    """
    Scratch PyTorch Implementation of PatchCore (Roth et al., CVPR 2022).
    - Extracts mid-level representations from layer2 and layer3 of ResNet/WideResNet.
    - Applies local neighborhood aggregation via AdaptiveAvgPool2d.
    - Uses greedy k-Center coreset subsampling with optional Johnson-Lindenstrauss random projection.
    - Computes pixel anomaly maps and nearest-neighbor anomaly scores.
    """
    def __init__(self, backbone_name: str = "wide_resnet50_2", coreset_ratio: float = 0.01, device: str = "cpu"):
        super().__init__()
        self.device = torch.device(device)
        self.coreset_ratio = coreset_ratio
        
        # Load backbone with ImageNet weights
        if backbone_name == "wide_resnet50_2":
            weights = models.Wide_ResNet50_2_Weights.DEFAULT
            self.backbone = models.wide_resnet50_2(weights=weights)
        elif backbone_name == "resnet18":
            weights = models.ResNet18_Weights.DEFAULT
            self.backbone = models.resnet18(weights=weights)
        else:
            raise ValueError(f"Unsupported backbone: {backbone_name}")
            
        self.backbone.to(self.device)
        self.backbone.eval()
        for p in self.backbone.parameters():
            p.requires_grad = False
            
        # Register feature hooks for layer2 and layer3
        self.features = {}
        def hook_fn(name):
            def hook(module, input, output):
                self.features[name] = output
            return hook
            
        self.backbone.layer2.register_forward_hook(hook_fn("layer2"))
        self.backbone.layer3.register_forward_hook(hook_fn("layer3"))
        
        self.memory_bank = None

    def _extract_patches(self, x: torch.Tensor):
        self.features.clear()
        _ = self.backbone(x)
        
        f2 = self.features["layer2"]
        f3 = self.features["layer3"]
        
        # Aggregate local neighborhood with 3x3 stride-1 avg pool
        avg_pool = nn.AvgPool2d(kernel_size=3, stride=1, padding=1)
        f2 = avg_pool(f2)
        f3 = avg_pool(f3)
        
        # Upsample f3 to match f2 spatial dimensions
        f3_upsampled = F.interpolate(f3, size=f2.shape[-2:], mode="bilinear", align_corners=False)
        
        # Concatenate multi-scale representations along channel dimension
        # Shape: (B, C1 + C2, H, W)
        patch_features = torch.cat([f2, f3_upsampled], dim=1)
        
        B, C, H, W = patch_features.shape
        # Permute to (B, H, W, C) -> reshape to (B * H * W, C)
        patch_tokens = patch_features.permute(0, 2, 3, 1).reshape(-1, C)
        return patch_tokens, (H, W)

    def fit(self, dataloader):
        """
        Extracts patch embeddings from normal training images and builds coreset memory bank.
        """
        all_patches = []
        print("[PatchCore] Extracting patch tokens from normal training set...")
        start_time = time.time()
        
        with torch.no_grad():
            for batch in dataloader:
                images = batch["image"].to(self.device)
                patches, _ = self._extract_patches(images)
                all_patches.append(patches.cpu())
                
        all_patches = torch.cat(all_patches, dim=0).numpy()
        extract_time = time.time() - start_time
        print(f"[PatchCore] Collected {all_patches.shape[0]} patch vectors (Dim: {all_patches.shape[1]}) in {extract_time:.2f}s")
        
        # Subsample using k-Center Greedy Coreset
        n_select = max(1, int(len(all_patches) * self.coreset_ratio))
        print(f"[PatchCore] Subsampling coreset to {n_select} patches (ratio: {self.coreset_ratio * 100:.1f}%)...")
        
        # Apply Johnson-Lindenstrauss projection for fast distance computation
        if all_patches.shape[1] > 128:
            srp = SparseRandomProjection(n_components=128, random_state=42)
            projected = srp.fit_transform(all_patches)
        else:
            projected = all_patches
            
        coreset_indices = self._k_center_greedy(projected, n_select)
        self.memory_bank = torch.tensor(all_patches[coreset_indices], dtype=torch.float32, device=self.device)
        print(f"[PatchCore] Memory bank initialized with shape: {tuple(self.memory_bank.shape)}")

    def _k_center_greedy(self, features: np.ndarray, n_select: int):
        """
        Fast Min-Max Euclidean greedy approximation for coreset selection.
        """
        N = features.shape[0]
        selected_idx = [np.random.RandomState(42).randint(0, N)]
        
        # Distance array to track min distance to currently selected centers
        dist_to_centers = np.linalg.norm(features - features[selected_idx[0]], axis=1)
        
        for _ in range(1, n_select):
            new_idx = np.argmax(dist_to_centers)
            selected_idx.append(new_idx)
            new_dist = np.linalg.norm(features - features[new_idx], axis=1)
            dist_to_centers = np.minimum(dist_to_centers, new_dist)
            
        return selected_idx

    def predict(self, image: torch.Tensor):
        """
        Inference on a single image tensor (1, 3, H, W).
        Returns:
            anomaly_score (float), anomaly_map (np.ndarray of shape (H, W)), latency_ms (float)
        """
        if self.memory_bank is None:
            raise RuntimeError("Model has not been fitted. Call fit() first.")
            
        t0 = time.perf_counter()
        with torch.no_grad():
            image = image.to(self.device)
            patches, (H, W) = self._extract_patches(image)
            
            # Compute Euclidean distance to memory bank: (N_patches, N_memory)
            diff = patches.unsqueeze(1) - self.memory_bank.unsqueeze(0)
            dists = torch.norm(diff, p=2, dim=2) # (N_patches, N_memory)
            
            # Patch score is the min distance to memory bank
            min_dists, _ = torch.min(dists, dim=1) # (N_patches,)
            
            # Anomaly map
            patch_scores = min_dists.reshape(1, 1, H, W)
            # Bilinear interpolation to original image size
            anomaly_map = F.interpolate(patch_scores, size=(image.shape[-2], image.shape[-1]), mode="bilinear", align_corners=False)
            anomaly_map = anomaly_map.squeeze().cpu().numpy()
            
            # Smooth anomaly map with Gaussian filter
            anomaly_map = gaussian_filter(anomaly_map, sigma=4)
            
            # Image-level anomaly score (max patch score)
            image_score = float(np.max(anomaly_map))
            
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return image_score, anomaly_map, latency_ms

if __name__ == "__main__":
    from dataset import MVTecDataset
    from torch.utils.data import DataLoader
    
    print("[Test] Initializing PatchCore with ResNet-18 (fast lightweight test)...")
    model = PatchCore(backbone_name="resnet18", coreset_ratio=0.01, device="cpu")
    
    train_ds = MVTecDataset("./data", "bottle", split="train")
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=False)
    
    model.fit(train_loader)
    
    test_ds = MVTecDataset("./data", "bottle", split="test")
    test_sample = test_ds[0] # Anomaly
    score, amap, lat = model.predict(test_sample["image"].unsqueeze(0))
    print(f"[Test] Anomaly Score: {score:.4f} | Latency: {lat:.1f}ms | Map Shape: {amap.shape}")
