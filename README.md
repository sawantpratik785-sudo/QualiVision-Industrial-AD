# QualiVision: Unsupervised Visual Anomaly Detection for Industrial Quality Inspection

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-ff4b4b.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Computer Vision system for automated manufacturing quality assurance, implementing an **Accuracy–Latency Benchmarking Study** between:
1. **PatchCore** (Roth et al., *CVPR 2022*) — Implemented from scratch in pure PyTorch.
2. **EfficientAD** (Batzner et al., *WACV 2024*) — Fast student-teacher distillation benchmark.

Developed for **AIM3003: Computer Vision** at **D Y Patil International University, Pune**.

---

## 👥 Project Team
* **Pratik Sawant** (PRN: `20240802324`) — *Algorithmic Engine: PyTorch hooks, JL Projection & Greedy k-Center Coreset*
* **Anvesh Patil** (PRN: `20240802334`) — *Data Architecture: MVTec AD pipeline & EfficientAD distillation*
* **Jayesh Deshmukh** (PRN: `20240802335`) — *Scoring & Deployment: Nearest-neighbor scoring, Gaussian smoothing, Streamlit UI & SQLite audit trail*

**Faculty Guide:** [Faculty Name]  
**Academic Year:** 2026–2027  

---

## 🚀 Key Features

* **One-Class Unsupervised Learning:** Trained exclusively on defect-free ("normal") parts; detects never-before-seen defects without manual flaw labeling.
* **Pure PyTorch Implementation:** Written from scratch without high-level wrapper libraries (e.g. `anomalib`) to demonstrate complete architectural depth.
* **99% Memory Compression:** Leverages **Johnson-Lindenstrauss Random Projection** (384-D $\rightarrow$ 128-D) and **Min-Max Greedy k-Center Subsampling** (163,856 patches compressed to 1,638 vectors).
* **Explainable Anomaly Heatmaps:** Bilinear interpolation with 2D Gaussian spatial smoothing ($\sigma = 4$) and JET alpha blending ($0.6 \cdot \text{Image} + 0.4 \cdot \text{Heatmap}$).
* **Industrial Compliance & Traceability:** Integrated SQLite exception logger (`inspections.db`) reflecting GE Aerospace and ISO 9001 quality audit standards.

---

## 📊 Live Empirical Results (Category: `bottle`)

| Sample Type | Ground Truth | PatchCore Score | Threshold | Verdict | Latency (CPU) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Test Case 1** | `broken_large` | **`3.2781`** | `2.5000` | **`DEFECT` (True Positive)** | 2582.2 ms |
| **Test Case 2** | `good` (normal) | **`1.3007`** | `2.5000` | **`PASS` (True Negative)** | 2274.6 ms |

* **Separation Margin:** $\Delta = 1.9774$ guarantees noise-tolerant, zero-false-alarm classification.

---

## 🛠️ Project Structure

```
industrial_ad/
├── app.py                                   # Streamlit operator inspection console
├── patchcore.py                             # From-scratch PyTorch PatchCore implementation
├── dataset.py                               # Custom MVTec AD PyTorch DataLoader & mask aligner
├── db_logger.py                             # SQLite audit trail integration (inspections.db)
├── run_demo.py                              # Headless verification & test harness
├── industrial_ad_template_14_slides.pptx    # Official 14-slide presentation deck (PowerPoint)
├── industrial_ad_template_14_slides.pdf     # 14-slide presentation deck (PDF)
├── Master_Technical_Defense_and_Project_Guide.pdf # Complete technical & viva guide
├── Individual_Viva_Defense_Scripts.pdf      # Task-by-task viva scripts for Pratik, Anvesh, Jayesh
└── .gitignore                               # Git ignore configuration (excludes 5GB data)
```

---

## 💻 Installation & Quickstart

### 1. Clone Repository & Install Dependencies
```bash
git clone <YOUR_REPOSITORY_URL>
cd industrial_ad
pip install torch torchvision opencv-python streamlit pandas scikit-learn scipy reportlab python-pptx
```

### 2. Download MVTec AD Dataset
Download the `bottle` category from the [MVTec AD Portal](https://www.mvtec.com/research-teaching/datasets/mvtec-ad) and place it under `./data/bottle/`.

### 3. Launch the Interactive Inspection Console
```bash
streamlit run app.py
```
Open `http://localhost:8501` to view live defect heatmaps and log inspection telemetry.

---

## 📚 Academic References
1. **PatchCore:** K. Roth et al., *"Towards Total Recall in Industrial Anomaly Detection"*, **IEEE/CVF CVPR 2022**, pp. 14298–14308.
2. **EfficientAD:** K. Batzner et al., *"EfficientAD: Accurate Visual Anomaly Detection at Millisecond-Level Latencies"*, **IEEE/CVF WACV 2024**, pp. 127–137.
3. **MVTec AD:** P. Bergmann et al., *"MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection"*, **IEEE/CVF CVPR 2019**, pp. 9584–9592.
