import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_templated_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    COLOR_DARK = RGBColor(15, 23, 42)      # Slate 900
    COLOR_NAVY = RGBColor(30, 41, 59)      # Slate 800
    COLOR_BLUE = RGBColor(37, 99, 235)     # Royal Blue
    COLOR_CYAN = RGBColor(6, 182, 212)     # Cyan
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_GRAY = RGBColor(100, 116, 139)   # Slate 500
    COLOR_LIGHT = RGBColor(248, 250, 252)  # Slate 50

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, slide_number_str):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        banner.fill.solid()
        banner.fill.fore_color.rgb = COLOR_DARK
        banner.line.color.rgb = COLOR_DARK

        tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(9.5), Inches(0.3))
        p_cat = tx_cat.text_frame.paragraphs[0]
        p_cat.text = "MINI PROJECT PRESENTATION — AIM3003: COMPUTER VISION"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_CYAN

        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(10.0), Inches(0.65))
        p_title = tx_title.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        tx_num = slide.shapes.add_textbox(Inches(11.5), Inches(0.25), Inches(1.2), Inches(0.65))
        p_num = tx_num.text_frame.paragraphs[0]
        p_num.text = slide_number_str
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.size = Pt(22)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_CYAN

    def add_card(slide, left, top, width, height, bg_color=COLOR_LIGHT, border_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    def create_two_column_slide(title, slide_num, col1_title, col1_bullets, col2_title, col2_bullets):
        slide = prs.slides.add_slide(blank_layout)
        add_header(slide, title, slide_num)

        add_card(slide, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.5), COLOR_LIGHT, COLOR_BLUE)
        tx1 = slide.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(5.1))
        tf1 = tx1.text_frame
        tf1.word_wrap = True
        p1 = tf1.paragraphs[0]
        p1.text = col1_title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_BLUE

        for b in col1_bullets:
            p = tf1.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(13)
            p.font.color.rgb = COLOR_NAVY
            p.space_before = Pt(8)

        add_card(slide, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.5), COLOR_LIGHT, COLOR_CYAN)
        tx2 = slide.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.1))
        tf2 = tx2.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = col2_title
        p2.font.size = Pt(17)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_DARK

        for b in col2_bullets:
            p = tf2.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(13)
            p.font.color.rgb = COLOR_NAVY
            p.space_before = Pt(8)

        return slide

    # =========================================================
    # SLIDE 01: TITLE SLIDE (Updated with 3 Specific Team Members)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_DARK
    bg1.line.color.rgb = COLOR_DARK

    t_box = s1.shapes.add_textbox(Inches(0.9), Inches(0.9), Inches(11.5), Inches(2.3))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Unsupervised Visual Anomaly Detection for Industrial Quality Inspection"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Accuracy–Latency Comparison of PatchCore and EfficientAD"
    p2.font.size = Pt(19)
    p2.font.color.rgb = COLOR_CYAN
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Mini Project Presentation"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_GRAY
    p3.space_before = Pt(6)

    # Submitted By Box (Updated to the 3 teammates)
    add_card(s1, Inches(0.9), Inches(3.6), Inches(5.6), Inches(3.1), COLOR_NAVY)
    card1_tx = s1.shapes.add_textbox(Inches(1.1), Inches(3.8), Inches(5.2), Inches(2.7))
    c1_tf = card1_tx.text_frame
    c1_tf.word_wrap = True
    p = c1_tf.paragraphs[0]
    p.text = "SUBMITTED BY:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    members = [
        "1. Pratik Sawant (PRN: 20240802324)",
        "2. Anvesh Patil (PRN: 20240802334)",
        "3. Jayesh Deshmukh (PRN: 20240802335)"
    ]
    for m in members:
        pm = c1_tf.add_paragraph()
        pm.text = m
        pm.font.size = Pt(14)
        pm.font.color.rgb = COLOR_WHITE
        pm.space_before = Pt(8)

    # Academic Meta Box
    add_card(s1, Inches(6.8), Inches(3.6), Inches(5.6), Inches(3.1), COLOR_NAVY)
    card2_tx = s1.shapes.add_textbox(Inches(7.0), Inches(3.8), Inches(5.2), Inches(2.7))
    c2_tf = card2_tx.text_frame
    c2_tf.word_wrap = True
    p = c2_tf.paragraphs[0]
    p.text = "ACADEMIC & GUIDE DETAILS:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    details = [
        "Class / Division: TY B.Tech (AI & ML)",
        "Department: School of Computer Science, Engineering & Applications",
        "Guided by: [Faculty In-Charge Name]",
        "Institution: D Y Patil International University, Pune",
        "Academic Year: 2026–2027"
    ]
    for d in details:
        pd = c2_tf.add_paragraph()
        pd.text = d
        pd.font.size = Pt(13)
        pd.font.color.rgb = COLOR_WHITE
        pd.space_before = Pt(6)

    # Slides 02 to 14
    create_two_column_slide(
        "Introduction", "02",
        "Project Background & Purpose",
        [
            "Industrial manufacturing requires strict zero-defect quality control across fast-moving production lines.",
            "Visual inspection is the primary barrier preventing flawed parts from reaching customers or critical assemblies.",
            "Our project introduces an automated computer vision inspection framework that detects surface anomalies without needing defective training data.",
            "We model the normal visual manifold using one-class unsupervised learning to identify unseen flaws."
        ],
        "Comparative Research Focus",
        [
            "Conducts an empirical accuracy-latency trade-off comparison between two state-of-the-art vision paradigms:",
            "1. PatchCore (Roth et al., CVPR 2022): Memory-bank non-parametric modeling with 0 training epochs.",
            "2. EfficientAD (Batzner et al., WACV 2024): Lightweight student-teacher distillation with sub-10ms latency.",
            "Delivers an interactive Streamlit dashboard with JET heatmaps and SQLite audit logging."
        ]
    )

    create_two_column_slide(
        "Problem Statement", "03",
        "The Core Problem & Current Practices",
        [
            "What problem does the project address? Detecting micro-cracks, scratches, contamination, and structural defects in industrial parts where defective samples are scarce.",
            "How is it handled currently? 1) Manual human visual inspection, which suffers from fatigue, high labor costs, and subjective inconsistency; and 2) Supervised deep learning (YOLO/CNNs).",
            "Supervised models require thousands of labeled defect examples and fail silently on novel defect forms."
        ],
        "Difficulties & Gaps Aimed to Reduce",
        [
            "Defect Scarcity Bottleneck: Factory scrap rates are <0.1%; collecting balanced defect datasets is economically impossible.",
            "Unbounded Flaw Variations: Defects take infinite unknown visual shapes.",
            "Accuracy-Latency Trade-off Gap: PatchCore provides ~99% AUROC but has high query latency; EfficientAD provides millisecond speed but requires heavy GPU training.",
            "Lack of Explainable Localization: Operators need pixel heatmaps, not just black-box PASS/FAIL labels."
        ]
    )

    create_two_column_slide(
        "Motivation", "04",
        "Why Choose This Project?",
        [
            "High Industry Impact: Visual inspection is a top-tier commercial application of computer vision in aerospace, automotive, and pharmaceuticals.",
            "Deep Algorithmic Value: Offers practical implementation experience with intermediate PyTorch layer hooks, dimensionality reduction, and greedy coreset algorithms.",
            "Safety-Critical Need: A single undetected defect in aircraft fasteners or medical vials causes severe failures, costly recalls, and life-safety hazards."
        ],
        "Who Benefits From This Project?",
        [
            "Quality Assurance Engineers: Automated 24/7 inspection with objective, mathematical consistency.",
            "Factory Floor Operators: Real-time visual heatmaps pinpointing exact flaw locations instantly.",
            "Manufacturing System Architects: Objective engineering data on whether to deploy memory banks or student-teacher models based on hardware constraints."
        ]
    )

    create_two_column_slide(
        "Objectives", "05",
        "Core Technical Objectives (1 - 3)",
        [
            "1. Design and Implement PatchCore from scratch in PyTorch, extracting multi-scale patch features from pre-trained convolutional backbones (layer2 and layer3) without wrapper libraries.",
            "2. Optimize the patch memory bank using Johnson-Lindenstrauss random projection and greedy k-Center coreset subsampling, achieving a 99% reduction in stored vectors.",
            "3. Validate and Compare PatchCore across all 15 MVTec AD categories and benchmark against EfficientAD across representative classes."
        ],
        "Applied & Deployment Objectives (4 - 5)",
        [
            "4. Calculate and Analyze standard industrial metrics: Image-level AUROC, Pixel-level AUROC, per-sample inference latency (ms), and GPU/CPU memory consumption.",
            "5. Develop and Display an interactive Streamlit inspection application featuring real-time JET defect heatmaps, PASS/DEFECT classification, and automated SQLite audit logging."
        ]
    )

    create_two_column_slide(
        "Scope", "06",
        "Features Included in Project Scope",
        [
            "Complete from-scratch PyTorch implementation of PatchCore (feature extraction, neighborhood pooling, greedy k-center).",
            "MVTec AD dataset ingestion (15 categories: 5 textures, 10 objects) with pixel-level ground truth mask alignment.",
            "Benchmarking EfficientAD student-teacher models on 5 representative categories (bottle, cable, capsule, metal_nut, transistor).",
            "Robustness evaluation under synthetic lighting shifts (+/- 20% brightness) and sample-size reduction (10%, 25%, 50%, 100%).",
            "Interactive Streamlit GUI with SQLite exception logging."
        ],
        "What is Outside the Project Scope",
        [
            "Physical camera hardware mounting and conveyor belt mechanical trigger integration.",
            "Industrial fieldbus communication protocols (e.g., Modbus, Profinet, EtherCAT).",
            "Full training of EfficientAD across all 15 categories due to academic GPU compute limits.",
            "3D point cloud and volumetric sensor processing (MVTec 3D-AD)."
        ]
    )

    create_two_column_slide(
        "Methodology", "07",
        "Data Pipeline & Feature Extraction",
        [
            "Step 1: Dataset Pipeline — Standardize MVTec AD images to 224x224, apply ImageNet normalization, and pair test anomalies with ground-truth binary masks.",
            "Step 2: Multi-Scale Patch Extraction — Attach PyTorch forward hooks to layer2 and layer3 of ResNet18/WideResNet50. Apply 3x3 stride-1 average pooling to aggregate local neighborhoods into 384-D patch tokens.",
            "Step 3: Coreset Memory Bank Construction — Project features to 128-D via Johnson-Lindenstrauss. Run Min-Max Greedy k-Center to compress 163,856 patches to 1,638 vectors (1.0% coreset)."
        ],
        "Distillation, Benchmarking & App",
        [
            "Step 4: EfficientAD Knowledge Distillation — Train student network and autoencoder to mimic a fixed pre-trained teacher network exclusively on normal parts.",
            "Step 5: Comparative Evaluation & Robustness Testing — Benchmark detection accuracy, millisecond latency, and few-shot degradation.",
            "Step 6: Dashboard & Audit Trail Deployment — Build Streamlit UI for visual inspection with automated SQLite logging."
        ]
    )

    create_two_column_slide(
        "Working Principle", "08",
        "Step-by-Step Workflow Mechanics",
        [
            "1. User Input: Operator uploads an inspection image or chooses an online sample from the MVTec AD test stream.",
            "2. Patch Extraction: Input image passes through convolutional backbone; multi-scale neighborhood patch descriptors are extracted.",
            "3. Distance Calculation: Each query patch computes Euclidean distance to its nearest neighbor in the stored normal memory bank: s_i = min || p_i - m ||.",
            "4. Heatmap Generation: Patch distances are bilinearly upsampled to 224x224 and smoothed using a 2D Gaussian filter (sigma = 4)."
        ],
        "Output Produced & Audit Logging",
        [
            "5. Visual Output: Anomaly map normalized and converted to a JET colormap overlay: Display = 0.6 * Image + 0.4 * Heatmap.",
            "6. Verdict Decision: Maximum patch distance represents image anomaly score. Score >= Threshold -> DEFECT; Score < Threshold -> PASS.",
            "7. Telemetry & Database Record: Automatically commits timestamp, part category, anomaly score, threshold, verdict, and latency into inspections.db."
        ]
    )

    create_two_column_slide(
        "Applications", "09",
        "High-Reliability Industrial Domains",
        [
            "Aerospace & Defense: Surface inspection of turbine blades, fastener integrity, composite panels, and machined engine casings.",
            "Pharmaceutical & Healthcare: Detection of cracked glass vials, particulate contamination in liquid medicine, and damaged blister packs.",
            "Semiconductor & PCB Manufacturing: Automated detection of short circuits, missing solder joints, bridge defects, and scratched wafers."
        ],
        "Automotive & Fast-Moving Consumer Goods",
        [
            "Automotive Assembly: Quality inspection of engine piston rings, brake discs, welded chassis seams, and exterior paint finish.",
            "Packaging & Bottling Lines: Monitoring bottle seal completeness, capping alignment, label positioning, and structural wall cracks.",
            "Textile & Material Production: Weave irregularities, surface abrasions, and color deviations in carpet, leather, and tile production."
        ]
    )

    create_two_column_slide(
        "Advantages", "10",
        "Algorithmic & Operational Benefits",
        [
            "1. Zero Defect Training Data Needed: Eliminates defect collection bottlenecks by learning entirely from normal, defect-free parts.",
            "2. Unseen Flaw Detection: Accurately flags novel, unexpected defect types that supervised classifiers miss.",
            "3. 99% Memory Reduction via Coreset Optimization: Greedy k-center reduces memory bank from 163,856 to 1,638 patches without performance loss."
        ],
        "Speed, Explainability & Traceability",
        [
            "4. Zero-Epoch Instant Deployment: PatchCore requires no backpropagation training, allowing immediate deployment.",
            "5. Pixel-Level Visual Explainability: Generates intuitive JET defect heatmaps rather than black-box binary decisions.",
            "6. Regulatory Compliance: Automated SQLite logging fulfills ISO 9001 and aerospace QA traceability standards."
        ]
    )

    create_two_column_slide(
        "Limitations", "11",
        "Computational & Architectural Constraints",
        [
            "1. Higher Latency on CPU Hardware: PatchCore nearest-neighbor search takes ~2.2 - 2.5 seconds on CPU, requiring GPU/INT8 quantization for fast conveyor speeds.",
            "2. Training Overhead for EfficientAD: Requires ~70,000 backpropagation iterations per category, requiring dedicated GPU training compute.",
            "3. Memory Footprint Scales with Categories: Storing separate patch banks for 15 classes requires substantial RAM/VRAM."
        ],
        "Visual & Environmental Sensitivity",
        [
            "4. Sensitivity to Extreme Misalignment: Large rotational misalignments or viewpoint changes can produce false alarms.",
            "5. 2D Surface Constraint: Cannot detect internal sub-surface voids or volumetric structural flaws that require X-ray/ultrasound sensors."
        ]
    )

    create_two_column_slide(
        "Conclusion", "12",
        "Summary of What Was Developed",
        [
            "Developed an end-to-end unsupervised visual defect inspection framework for industrial quality control.",
            "Implemented PatchCore from scratch in PyTorch with multi-scale layer hooks and greedy k-Center subsampling.",
            "Built a functional Streamlit inspection interface with real-time JET heatmaps and automated SQLite audit logging.",
            "Established a clear empirical baseline comparing memory-bank methods against student-teacher networks."
        ],
        "Objectives Met & Main Learning Outcomes",
        [
            "Objectives Achieved: All 5 primary objectives achieved—scratch implementation, 99% coreset reduction, empirical validation, metric evaluation, and GUI deployment.",
            "Empirical Validation: Verified clean separation on MVTec 'bottle' (Defect score: 3.28 vs Normal score: 1.30 against threshold 2.50).",
            "Key Learning: Mastered the practical engineering trade-offs between zero-shot memory-bank accuracy and millisecond distillation latency."
        ]
    )

    create_two_column_slide(
        "Future Scope", "13",
        "Edge Deployment & Architectural Improvements",
        [
            "1. Edge Hardware Quantization: Apply INT8 post-training quantization and TensorRT compilation to drop CPU latency from ~2500ms to <50ms for Raspberry Pi / Jetson deployment.",
            "2. Unified Multi-Class Model: Develop a single unified memory bank / distillation network that inspects all 15 MVTec classes simultaneously without switching checkpoints.",
            "3. 3D Vision & Point Cloud Integration: Expand framework to MVTec 3D-AD by fusing RGB images with depth point clouds to detect 3D surface dents."
        ],
        "Factory Automation & PLC Connectivity",
        [
            "4. Industrial PLC Bus Integration: Connect SQLite audit logger to industrial communication protocols (Modbus / OPC-UA) to trigger pneumatic rejection arms on factory sorters.",
            "5. Active Learning Feedback Loop: Enable quality operators to confirm false alarms, dynamically updating the coreset memory bank."
        ]
    )

    # Slide 14: References
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "References", "14")
    add_card(s14, Inches(0.8), Inches(1.45), Inches(11.733), Inches(5.5), COLOR_LIGHT)

    tx14 = s14.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(5.1))
    tf14 = tx14.text_frame
    tf14.word_wrap = True

    refs = [
        ("1. PatchCore (Main Benchmark Paper):", "Roth, K., Pemula, L., Zepeda, J., Schölkopf, B., Brox, T., & Gehler, P. (2022). Towards Total Recall in Industrial Anomaly Detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 14298–14308."),
        ("2. EfficientAD (Comparison Architecture):", "Batzner, K., Heckler, L., & König, R. (2024). EfficientAD: Accurate Visual Anomaly Detection at Millisecond-Level Latencies. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), pp. 127–137."),
        ("3. MVTec AD (Benchmark Dataset):", "Bergmann, P., Fauser, M., Sattlegger, D., & Steger, C. (2019). MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 9584–9592."),
        ("4. PaDiM (Baseline Comparison):", "Defard, T., Setkov, A., Loesch, A., & Audigier, R. (2021). PaDiM: A Patch Distribution Modeling Framework for Anomaly Detection and Localization. In International Conference on Pattern Recognition (ICPR Workshops), Springer LNCS 12664, pp. 475–489."),
        ("5. VisA (Benchmark Dataset & Self-Supervision):", "Zou, Y., Jeong, J., Pemula, L., Zhang, D., & Dhome, M. (2022). SPot-the-Difference: Self-Supervised Pre-training for Anomaly Detection and Segmentation (VisA). In European Conference on Computer Vision (ECCV), Springer LNCS 13690, pp. 392–408.")
    ]

    for label, cite in refs:
        p_lbl = tf14.add_paragraph()
        p_lbl.text = label
        p_lbl.font.size = Pt(13)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_BLUE
        p_lbl.space_before = Pt(6)

        p_c = tf14.add_paragraph()
        p_c.text = cite
        p_c.font.size = Pt(12)
        p_c.font.color.rgb = COLOR_NAVY

    output_path = r"C:\Users\Lenovo\.gemini\antigravity\scratch\industrial_ad\industrial_ad_template_14_slides.pptx"
    prs.save(output_path)
    print("Updated presentation saved successfully with 3 members at:", output_path)

if __name__ == "__main__":
    create_templated_presentation()
