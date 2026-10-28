import os
from glob import glob
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class MVTecDataset(Dataset):
    """
    Standard MVTec AD Dataset loader.
    Supports train (unsupervised, only 'good') and test (good + defect types).
    Returns image, label (0=normal, 1=anomaly), mask (pixel ground truth), and metadata.
    """
    def __init__(self, root_dir: str, category: str, split: str = "train", img_size: int = 224):
        self.root_dir = os.path.join(root_dir, category)
        self.split = split
        self.img_size = img_size
        
        self.transform_img = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.transform_mask = transforms.Compose([
            transforms.Resize((img_size, img_size), interpolation=transforms.InterpolationMode.NEAREST),
            transforms.ToTensor()
        ])
        
        self.img_paths = []
        self.labels = []
        self.mask_paths = []
        self.defect_types = []
        
        self._load_samples()

    def _load_samples(self):
        split_dir = os.path.join(self.root_dir, self.split)
        defect_types = sorted(os.listdir(split_dir))
        
        for defect in defect_types:
            defect_folder = os.path.join(split_dir, defect)
            if not os.path.isdir(defect_folder):
                continue
                
            img_files = sorted(glob(os.path.join(defect_folder, "*.png")))
            for img_path in img_files:
                self.img_paths.append(img_path)
                self.defect_types.append(defect)
                
                if defect == "good":
                    self.labels.append(0)
                    self.mask_paths.append(None)
                else:
                    self.labels.append(1)
                    # Ground truth mask mapping:
                    # bottle/ground_truth/<defect>/<idx>_mask.png
                    img_name = os.path.splitext(os.path.basename(img_path))[0]
                    mask_path = os.path.join(self.root_dir, "ground_truth", defect, f"{img_name}_mask.png")
                    self.mask_paths.append(mask_path)

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        img = Image.open(img_path).convert("RGB")
        img_tensor = self.transform_img(img)
        label = self.labels[idx]
        
        if self.mask_paths[idx] and os.path.exists(self.mask_paths[idx]):
            mask = Image.open(self.mask_paths[idx]).convert("L")
            mask_tensor = self.transform_mask(mask)
            mask_tensor = (mask_tensor > 0.5).float()
        else:
            mask_tensor = torch.zeros((1, self.img_size, self.img_size), dtype=torch.float32)

        return {
            "image": img_tensor,
            "label": label,
            "mask": mask_tensor,
            "defect_type": self.defect_types[idx],
            "path": img_path
        }

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "./data"
    category = "bottle"
    if os.path.exists(os.path.join(data_dir, category)):
        train_ds = MVTecDataset(data_dir, category, split="train")
        test_ds = MVTecDataset(data_dir, category, split="test")
        print(f"[{category}] Train samples (good only): {len(train_ds)}")
        print(f"[{category}] Test samples (good + defects): {len(test_ds)}")
        sample = test_ds[0]
        print(f"Sample tensor shape: {sample['image'].shape}, Label: {sample['label']}, Defect: {sample['defect_type']}")
    else:
        print(f"Category folder not found yet: {os.path.join(data_dir, category)}")
