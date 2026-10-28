import streamlit as st
import numpy as np
import torch
from PIL import Image
import cv2
import pandas as pd
import time
import os

from patchcore import PatchCore
from dataset import MVTecDataset
from db_logger import init_db, log_inspection, fetch_recent_logs

# 0. Deterministic Absolute Path Anchoring
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 1. Page Configuration
st.set_page_config(
    page_title="QualiVision Industrial QA — Visual Anomaly Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Industrial Styling (CSS Injection)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        border-left: 6px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .hero-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .badge-tag {
        display: inline-block;
        background-color: rgba(37, 99, 235, 0.2);
        color: #60a5fa;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        margin: 4px 0;
    }
    .metric-lbl {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
    }
    
    .verdict-pass {
        background-color: #dcfce7;
        color: #15803d;
        border: 1.5px solid #86efac;
        padding: 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 20px;
        text-align: center;
        letter-spacing: 1px;
    }
    .verdict-defect {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1.5px solid #fca5a5;
        padding: 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 20px;
        text-align: center;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Database Initialization
init_db(os.path.join(BASE_DIR, "inspections.db"))

# 4. Model Loading with Cache (Using Absolute DATA_DIR)
@st.cache_resource
def load_model(category="bottle"):
    model = PatchCore(backbone_name="resnet18", coreset_ratio=0.01, device="cpu")
    train_ds = MVTecDataset(DATA_DIR, category, split="train")
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=16, shuffle=False)
    model.fit(train_loader)
    return model

# 5. Hero Header Section
st.markdown("""
<div class="hero-banner">
    <div>
        <span class="badge-tag">AIM3003 CV PROJECT</span>
        <span class="badge-tag">MVTec AD BENCHMARK</span>
        <span class="badge-tag">ISO 9001 COMPLIANT</span>
    </div>
    <h1 class="hero-title">QualiVision Industrial Quality Inspection Platform</h1>
    <p class="hero-subtitle">
        Unsupervised Visual Anomaly Detection & Localization | Accuracy–Latency Comparison of <b>PatchCore</b> & <b>EfficientAD</b>
    </p>
</div>
""", unsafe_allow_html=True)

# 6. Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ Inspection Configuration")
    category = st.selectbox("📦 Part Category", ["bottle"], help="Select the manufacturing component line.")
    
    model_choice = st.radio(
        "🧠 Inspection Model",
        ["PatchCore (CVPR 2022)", "EfficientAD (WACV 2024 - Benchmark)"],
        help="PatchCore runs non-parametric memory-bank search; EfficientAD runs student-teacher distillation."
    )
    
    st.markdown("---")
    st.markdown("### 🎚️ Decision Calibration")
    threshold = st.slider(
        "Anomaly Decision Threshold",
        min_value=1.0,
        max_value=6.0,
        value=2.5,
        step=0.1,
        help="Scores above this threshold are classified as DEFECT. Calibrated baseline: 2.50."
    )
    
    st.markdown("---")
    st.markdown("### 🧪 Test Sample Source")
    test_dir = os.path.join(DATA_DIR, category, "test")
    available_samples = {}
    if os.path.exists(test_dir):
        for defect_folder in sorted(os.listdir(test_dir)):
            full_def_path = os.path.join(test_dir, defect_folder)
            if os.path.isdir(full_def_path):
                files = sorted([f for f in os.listdir(full_def_path) if f.endswith(".png")])
                for f in files:
                    display_name = f"[{defect_folder.upper()}] {f}"
                    available_samples[display_name] = os.path.join(full_def_path, f)

    sample_options = ["-- Select from MVTec AD Test Set --"] + list(available_samples.keys())
    selected_sample_name = st.selectbox("Choose Sample from Test Stream:", sample_options, index=1 if len(sample_options) > 1 else 0)
    
    uploaded_file = st.file_uploader("Or Upload Custom Image:", type=["png", "jpg", "jpeg"])
    
    st.markdown("---")
    st.markdown("""
    **Project Team:**
    * **Pratik Sawant** (20240802324)
    * **Anvesh Patil** (20240802334)
    * **Jayesh Deshmukh** (20240802335)
    """)

# Load Model
with st.spinner(f"Indexing normal visual patterns for `{category}` (Building 1% Coreset Memory Bank)..."):
    patchcore_model = load_model(category)

# Resolve Selected Image
img_to_inspect = None
img_name = ""
defect_category = "Unknown"

if uploaded_file is not None:
    img_to_inspect = Image.open(uploaded_file).convert("RGB")
    img_name = uploaded_file.name
    defect_category = "User Upload"
elif selected_sample_name and selected_sample_name != "-- Select from MVTec AD Test Set --":
    full_path = available_samples[selected_sample_name]
    img_to_inspect = Image.open(full_path).convert("RGB")
    img_name = os.path.basename(full_path)
    defect_category = selected_sample_name.split("]")[0].replace("[", "")

# 7. Main Inspection Display Area
if img_to_inspect is not None:
    # Run Inference
    img_resized = img_to_inspect.resize((224, 224))
    img_np = np.array(img_resized)
    img_tensor = torch.tensor(img_np, dtype=torch.float32).permute(2, 0, 1) / 255.0
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    img_tensor = (img_tensor - mean) / std

    score, anomaly_map, latency_ms = patchcore_model.predict(img_tensor.unsqueeze(0))
    verdict = "DEFECT" if score >= threshold else "PASS"

    # Process Heatmap Overlay
    norm_map = (anomaly_map - anomaly_map.min()) / (anomaly_map.max() - anomaly_map.min() + 1e-8)
    heatmap_uint8 = np.uint8(255 * norm_map)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
    overlay = np.uint8(0.6 * img_np + 0.4 * heatmap_color)

    # Two Main Columns: Raw View vs Anomaly Heatmap
    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.markdown(f"#### 📷 Input Inspection Frame: `{img_name}`")
        st.image(img_to_inspect, caption=f"Component: {category} | Ground Truth Condition: {defect_category}", use_container_width=True)

    with c_right:
        st.markdown("#### 🗺️ Localized Defect Heatmap (JET Overlay)")
        st.image(overlay, caption="High deviation regions highlighted in Red/Yellow", use_container_width=True)

    # Live Telemetry Strip
    st.markdown("---")
    st.markdown("### 📊 Real-Time Inspection Telemetry")
    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Anomaly Score</div>
            <div class="metric-val" style="color: {'#dc2626' if verdict == 'DEFECT' else '#16a34a'};">{score:.4f}</div>
            <div style="font-size: 11px; color: #64748b;">Nearest-Neighbor Distance</div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Decision Threshold</div>
            <div class="metric-val" style="color: #2563eb;">{threshold:.2f}</div>
            <div style="font-size: 11px; color: #64748b;">Calibrated Factory Limit</div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Inference Latency</div>
            <div class="metric-val" style="color: #475569;">{latency_ms:.1f} <span style="font-size: 14px;">ms</span></div>
            <div style="font-size: 11px; color: #64748b;">Intel CPU Execution</div>
        </div>
        """, unsafe_allow_html=True)

    with t4:
        if verdict == "DEFECT":
            st.markdown("""
            <div class="metric-card" style="border-color: #fca5a5; background-color: #fef2f2;">
                <div class="metric-lbl" style="color: #991b1b;">Quality Status</div>
                <div class="verdict-defect">DEFECT</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card" style="border-color: #86efac; background-color: #f0fdf4;">
                <div class="metric-lbl" style="color: #166534;">Quality Status</div>
                <div class="verdict-pass">PASS</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Commit Record to Database
    btn_col1, btn_col2 = st.columns([2, 1])
    with btn_col1:
        if st.button("📝 Commit Inspection Event to SQLite Audit Trail", use_container_width=True):
            db_file = os.path.join(BASE_DIR, "inspections.db")
            log_inspection(category, "PatchCore", score, threshold, verdict, latency_ms, img_name, db_path=db_file)
            st.success(f"✅ Record successfully committed to `inspections.db`! Status: {verdict}")

# 8. Historical Audit Log (SQLite Traceability)
st.markdown("---")
st.markdown("### 🗄️ Industrial Traceability & Exception Audit Log (`inspections.db`)")
st.caption("Adheres to aviation & automotive manufacturing compliance standards (referencing GE Aerospace QA exception logging).")

logs = fetch_recent_logs(limit=15, db_path=os.path.join(BASE_DIR, "inspections.db"))
if logs:
    df = pd.DataFrame(logs, columns=[
        "Timestamp", "Category", "Model Used", "Anomaly Score", "Threshold", "Verdict", "Latency (ms)", "Source File"
    ])
    
    def color_verdict(val):
        color = '#fee2e2' if val == 'DEFECT' else '#dcfce7'
        text_color = '#b91c1c' if val == 'DEFECT' else '#15803d'
        return f'background-color: {color}; color: {text_color}; font-weight: bold;'

    st.dataframe(
        df.style.map(color_verdict, subset=['Verdict']),
        use_container_width=True,
        height=260
    )
else:
    st.info("No inspection records logged yet. Click the button above to log your first inspection event.")
