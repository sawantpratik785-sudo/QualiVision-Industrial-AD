# Individual Viva Defense & Code Implementation Master Scripts
## AIM3003 Computer Vision — Mini Project Viva Defense
**Project:** Unsupervised Visual Anomaly Detection for Industrial Quality Inspection (PatchCore vs. EfficientAD)

---

# STUDENT 1: PRATIK SAWANT (PRN: 20240802324)
### Assigned Objectives & Code Tasks:
* **Task `O2-T1`:** Multi-scale feature extraction without wrapper libraries (PyTorch Layer Hooks on `layer2` & `layer3` with $3 \times 3$ neighborhood pooling in `patchcore.py`).
* **Task `O2-T2`:** 99% memory compression via Johnson-Lindenstrauss random projection & Min-Max Greedy k-Center coreset subsampling.

---

## 1. Pratik's 90-Second Opening Explanation (Say this when asked "What did YOU do?")
> *"Good morning respected panel. In our project, my core responsibility was the algorithmic engine of PatchCore in `patchcore.py`. 
> 
> First, for task `O2-T1`, I implemented multi-scale patch feature extraction from scratch using PyTorch forward hooks. Rather than taking the final classification layer—which discards spatial information—I intercepted intermediate representations from `layer2` and `layer3` of ResNet-18. I then applied a 3x3 stride-1 average pooling layer to incorporate local spatial context into every patch.
> 
> Second, for task `O2-T2`, extracting patches across 209 normal training bottles generated 163,856 high-dimensional vectors (each 384-D). Storing all of them causes massive memory overhead and query latency. To solve this, I implemented dimensionality reduction using the Johnson-Lindenstrauss lemma down to 128 dimensions, followed by the Min-Max Greedy k-Center coreset algorithm. This compressed our memory bank by 99%—from 163,856 down to just 1,638 representative vectors—with virtually zero loss in detection accuracy."*

---

## 2. Pratik's Code Walkthrough (When the professor says "Show me your code")
Open `patchcore.py` and point your finger to these specific lines:

### A. The Forward Hooks (`patchcore.py`, lines 37–45):
```python
self.features = {}
def hook_fn(name):
    def hook(module, input, output):
        self.features[name] = output
    return hook

self.backbone.layer2.register_forward_hook(hook_fn("layer2"))
self.backbone.layer3.register_forward_hook(hook_fn("layer3"))
```
* **Explain:** *"Here, I attach forward hooks to ResNet's `layer2` and `layer3`. As the image passes through the CNN, PyTorch intercepts the intermediate tensor activations into my `self.features` dictionary without breaking the forward pass."*

### B. Neighborhood Pooling & Multi-Scale Concatenation (`patchcore.py`, lines 52–65):
```python
avg_pool = nn.AvgPool2d(kernel_size=3, stride=1, padding=1)
f2 = avg_pool(f2)
f3 = avg_pool(f3)
f3_upsampled = F.interpolate(f3, size=f2.shape[-2:], mode="bilinear", align_corners=False)
patch_features = torch.cat([f2, f3_upsampled], dim=1)
```
* **Explain:** *"I pass both layers through a 3x3 average pool with stride 1. This blends each patch with its 8 immediate spatial neighbors, making the representation robust to small camera alignment shifts. Because `layer3` has half the spatial resolution of `layer2`, I bilinearly upsample `f3` to match `f2` and concatenate them along the channel dimension, giving a 384-dimensional descriptor for each patch."*

### C. Johnson-Lindenstrauss Projection & Greedy k-Center (`patchcore.py`, lines 95–130):
```python
srp = SparseRandomProjection(n_components=128, random_state=42)
projected = srp.fit_transform(all_patches)

def _k_center_greedy(self, features, n_select):
    selected_idx = [np.random.RandomState(42).randint(0, N)]
    dist_to_centers = np.linalg.norm(features - features[selected_idx[0]], axis=1)
    for _ in range(1, n_select):
        new_idx = np.argmax(dist_to_centers)
        selected_idx.append(new_idx)
        new_dist = np.linalg.norm(features - features[new_idx], axis=1)
        dist_to_centers = np.minimum(dist_to_centers, new_dist)
    return selected_idx
```
* **Explain:** *"First, I use `SparseRandomProjection` to reduce dimensions from 384 to 128. Then in `_k_center_greedy`, I initialize one center randomly. At each iteration, I find the sample whose minimum distance to existing centers is maximum (`np.argmax(dist_to_centers)`). This ensures the selected 1,638 centers cover the outer boundary and interior of the normal manifold without redundant duplicate patches."*

---

## 3. Pratik's Viva Defense Questions & Answers

* **Q: Why didn't you use `layer4` (the deepest layer)?**
  * **Answer:** *"Sir, `layer4` has a spatial downsampling of 32x. A 224x224 image becomes just 7x7 pixels. The receptive field is too large, meaning spatial resolution is lost and we cannot pinpoint small 2mm cracks. Furthermore, `layer4` is heavily biased towards ImageNet object classification categories rather than generic surface textures."*
* **Q: What is the mathematical guarantee of the Johnson-Lindenstrauss lemma?**
  * **Answer:** *"The lemma guarantees that any metric space of $N$ points can be linearly embedded into $k = \mathcal{O}(\epsilon^{-2} \log N)$ dimensions while preserving pairwise Euclidean distances within a factor of $(1 \pm \epsilon)$. It ensures distance calculations in 128-D reflect true distances in 384-D with negligible distortion."*
* **Q: Why not just use K-Means clustering instead of Greedy k-Center?**
  * **Answer:** *"K-Means optimizes the mean squared error (centroids), which tends to average out rare features and pull centers toward dense clusters. In anomaly detection, rare normal patterns (like bottle neck threads) are critical. Greedy k-Center minimizes the maximum distance (min-max radius), guaranteeing that even rare normal edge cases are covered by at least one center."*

---
---

# STUDENT 2: ANVESH PATIL (PRN: 20240802334)
### Assigned Objectives & Code Tasks:
* **Task `O1-T1`:** Ingest and preprocess industrial defect benchmark (`dataset.py`, custom PyTorch DataLoader, and pixel-level ground-truth mask pairing).
* **Task `O4-T1`:** Student-Teacher distillation benchmarking (EfficientAD architecture configuration, comparison against PatchCore on 5 representative classes).

---

## 1. Anvesh's 90-Second Opening Explanation (Say this when asked "What did YOU do?")
> *"Good morning respected faculty. My primary responsibilities covered dataset architecture engineering in `dataset.py` and the EfficientAD distillation comparison framework for task `O4-T1`.
> 
> For task `O1-T1`, the standard torchvision `ImageFolder` class cannot handle MVTec AD because the directory structure is non-standard: test images are grouped by defect types (`broken_large`, `contamination`), while ground-truth pixel masks are stored in a parallel directory tree. I wrote `dataset.py` from scratch to automatically pair every defective test image with its corresponding 1-channel binary mask, while applying ImageNet normalization and nearest-neighbor mask resizing.
> 
> For task `O4-T1`, I analyzed and benchmarked EfficientAD. While PatchCore is a memory-bank method with zero training epochs, its query latency is high. EfficientAD solves this by using a pre-trained Teacher Network and training a Student Network to mimic the Teacher on normal images. I configured the 5-class evaluation pipeline (*bottle, cable, capsule, metal_nut, transistor*) to measure the trade-off between PatchCore's memory lookups and EfficientAD's sub-10ms forward passes."*

---

## 2. Anvesh's Code Walkthrough (When the professor says "Show me your code")
Open `dataset.py` and highlight these sections:

### A. Ground-Truth Mask Pairing Logic (`dataset.py`, lines 40–55):
```python
if defect == "good":
    self.labels.append(0)
    self.mask_paths.append(None)
else:
    self.labels.append(1)
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    mask_path = os.path.join(self.root_dir, "ground_truth", defect, f"{img_name}_mask.png")
    self.mask_paths.append(mask_path)
```
* **Explain:** *"In this loop, I scan the directory tree. If the folder is `good`, I assign label 0 and no mask. If it's a defect subfolder, I extract the base filename and map it to `ground_truth/<defect>/<name>_mask.png`. This ensures that during evaluation, we can calculate Pixel-level AUROC and Per-Region Overlap (PRO) against the ground-truth annotation."*

### B. Nearest-Neighbor Binary Mask Transform (`dataset.py`, lines 22–27):
```python
self.transform_mask = transforms.Compose([
    transforms.Resize((img_size, img_size), interpolation=transforms.InterpolationMode.NEAREST),
    transforms.ToTensor()
])
```
* **Explain:** *"Notice that for images I use standard bilinear resizing, but for masks I explicitly set `InterpolationMode.NEAREST`. If you use bilinear interpolation on a mask, pixels on the boundary become fractional floats like 0.3 or 0.7. Nearest-neighbor preserves strict binary values: 0 for background, 1 for defect."*

### C. Normalization Hyperparameters (`dataset.py`, line 19):
```python
transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
```
* **Explain:** *"These are the channel-wise means and standard deviations of the 1.28 million natural images in ImageNet. Because our feature extractor backbone was pre-trained on ImageNet, we must normalize incoming industrial frames to match this exact input distribution so the pre-trained convolutional filters activate properly."*

---

## 3. Anvesh's Viva Defense Questions & Answers

* **Q: Why can't we train EfficientAD on all 15 MVTec categories?**
  * **Answer:** *"PatchCore is non-parametric—it stores coreset patches with zero training epochs, taking only ~15 seconds per class. EfficientAD requires full backpropagation training of a Student network and an Autoencoder across ~70,000 iterations per category. Training all 15 classes requires massive GPU compute. Training on 5 representative categories (both objects and textures) provides complete empirical trade-off data within our academic timeline."*
* **Q: How does EfficientAD detect anomalies if it has no memory bank?**
  * **Answer:** *"EfficientAD uses knowledge distillation. The Teacher network is fixed and pre-trained on ImageNet. The Student network is trained via backpropagation strictly on normal images to predict the Teacher's output. When a normal image is passed, the Student mimics the Teacher (difference $\approx 0$). When a defective crack appears, the Student fails to predict the Teacher's output because it has never seen cracks before. The squared error between Student and Teacher forms the anomaly map in a single forward pass without any database lookup."*
* **Q: What is the purpose of the Autoencoder in EfficientAD?**
  * **Answer:** *"The student network can sometimes generalize too well and accidentally mimic the teacher even on anomalous textures. The autoencoder branch is trained to reconstruct normal features through a bottleneck, catching structural and logical anomalies (like missing parts or inverted components) that the student might overlook."*

---
---

# STUDENT 3: JAYESH DESHMUKH (PRN: 20240802335)
### Assigned Objectives & Code Tasks:
* **Task `O3-T1`:** Anomaly scoring, distance calculation, and 2D Gaussian spatial smoothing (`predict()` in `patchcore.py`).
* **Task `O5-T1`:** Industrial QA operator interface and SQLite exception audit logging (`app.py` & `db_logger.py`).

---

## 1. Jayesh's 90-Second Opening Explanation (Say this when asked "What did YOU do?")
> *"Good morning respected panel. My focus in this project was the inference scoring pipeline for task `O3-T1` and the complete deployment architecture for task `O5-T1`.
> 
> For task `O3-T1`, I implemented the nearest-neighbor distance computation in `patchcore.py`. For every query patch in a test image, my code computes the Euclidean distance to the nearest patch in Pratik's memory bank. I then interpolate this distance grid back to the original 224x224 resolution and apply a 2D Gaussian filter ($\sigma = 4$) using SciPy. This eliminates high-frequency noise spikes and produces smooth, contiguous anomaly heatmaps. On our test run, defective bottles scored 3.28 while normal bottles scored 1.30, providing a clean 1.98 decision margin.
> 
> For task `O5-T1`, I built our interactive Streamlit application (`app.py`) and integrated an ACID-compliant SQLite audit trail (`db_logger.py`) following GE Aerospace exception logging standards. This allows factory operators to inspect parts, view live JET heatmap overlays, adjust decision thresholds, and permanently record inspection events for ISO 9001 quality audits."*

---

## 2. Jayesh's Code Walkthrough (When the professor says "Show me your code")
Open `patchcore.py` and `db_logger.py` and show these lines:

### A. Nearest-Neighbor Scoring & Gaussian Smoothing (`patchcore.py`, lines 135–155):
```python
diff = patches.unsqueeze(1) - self.memory_bank.unsqueeze(0)
dists = torch.norm(diff, p=2, dim=2)
min_dists, _ = torch.min(dists, dim=1)

patch_scores = min_dists.reshape(1, 1, H, W)
anomaly_map = F.interpolate(patch_scores, size=(image.shape[-2], image.shape[-1]), mode="bilinear", align_corners=False)
anomaly_map = gaussian_filter(anomaly_map.squeeze().cpu().numpy(), sigma=4)
image_score = float(np.max(anomaly_map))
```
* **Explain:** *"Here, I compute the pairwise Euclidean distance between each query patch and all vectors in the coreset memory bank. The minimum distance represents the patch anomaly score. I upsample this coarse grid to 224x224 and convolve it with `gaussian_filter(..., sigma=4)`. The maximum value in the smoothed map becomes the overall image anomaly score."*

### B. SQLite Audit Trail Schema (`db_logger.py`, lines 7–22):
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inspection_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        part_category TEXT NOT NULL,
        model_used TEXT NOT NULL,
        anomaly_score REAL NOT NULL,
        threshold REAL NOT NULL,
        verdict TEXT NOT NULL,
        latency_ms REAL NOT NULL,
        image_name TEXT
    )
""")
```
* **Explain:** *"This function initializes `inspections.db`. Every time a part is inspected, we log the exact timestamp, part type, model used, raw anomaly score, threshold, final verdict (PASS/DEFECT), latency in milliseconds, and filename. This provides full traceability for manufacturing compliance."*

### C. Streamlit Alpha Blending (`app.py`, lines 80–90):
```python
norm_map = (anomaly_map - anomaly_map.min()) / (anomaly_map.max() - anomaly_map.min() + 1e-8)
heatmap_uint8 = np.uint8(255 * norm_map)
heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
overlay = np.uint8(0.6 * img_np + 0.4 * heatmap_color)
st.image(overlay, use_container_width=True)
```
* **Explain:** *"To give operators visual explainability, I normalize the anomaly map to [0, 255] and apply OpenCV's JET colormap. Then I alpha-blend 60% of the raw image with 40% of the heatmap overlay so the operator can clearly see the physical part texture underneath the red defect highlight."*

---

## 3. Jayesh's Viva Defense Questions & Answers

* **Q: Why apply Gaussian smoothing? Why not display the raw distance map?**
  * **Answer:** *"The raw nearest-neighbor scores exist on a coarse 28x28 grid. Bilinear upsampling alone produces jagged, blocky artifacts and single-pixel false alarms caused by sensor noise. A 2D Gaussian filter ($\sigma = 4$) smooths out high-frequency noise spikes, creating a coherent, continuous defect contour that accurately isolates the flaw."*
* **Q: Why use SQLite instead of a flat CSV file or MongoDB?**
  * **Answer:** *"In industrial QA lines, multiple inspection threads write telemetry simultaneously. A flat CSV file lacks ACID transactions and will corrupt during simultaneous file-write operations. MongoDB or PostgreSQL require separate background database servers, introducing network latency and maintenance overhead. SQLite is serverless, zero-configuration, ACID-compliant, and embeds directly into industrial edge PC terminals."*
* **Q: How did you select the 2.50 threshold?**
  * **Answer:** *"In our empirical testing on the MVTec bottle dataset, normal bottles scored around $1.30$, while defective bottles (`broken_large`) scored $3.28$. Setting our decision threshold at $2.50$ places the boundary directly in the middle of our $1.98$ margin, providing maximum tolerance against camera sensor fluctuations."*

---
---

# SUMMARY: WHO OWNS WHAT ON VIVA DAY

| Student Name | Assigned Code Files | Core Concepts to Defend |
| :--- | :--- | :--- |
| **Pratik Sawant** | `patchcore.py` (Feature Extraction & Coreset) | PyTorch forward hooks, Layer 2 & 3 rationale, 3x3 local pooling, Johnson-Lindenstrauss lemma, Min-Max Greedy k-Center coreset algorithm. |
| **Anvesh Patil** | `dataset.py` & EfficientAD benchmark | MVTec AD structure, nearest-neighbor mask interpolation, ImageNet normalization, Student-Teacher distillation, Autoencoder branch. |
| **Jayesh Deshmukh** | `app.py`, `db_logger.py`, & `predict()` in `patchcore.py` | Pairwise Euclidean distance scoring, 2D Gaussian filtering ($\sigma=4$), JET colormap alpha blending, Streamlit dashboard, SQLite ACID compliance. |
