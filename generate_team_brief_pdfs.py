import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas


def make_canvas_class(header_left: str, header_right: str):
    class MemberNumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_header_footer(num_pages)
                super().showPage()
            super().save()

        def draw_header_footer(self, page_count):
            self.saveState()
            if self._pageNumber > 1:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(HexColor("#64748b"))
                self.drawString(54, 752, header_left)
                self.drawRightString(558, 752, header_right)
                self.setStrokeColor(HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(54, 744, 558, 744)

            self.setFont("Helvetica", 8)
            self.setFillColor(HexColor("#64748b"))
            self.drawString(54, 34, "AIM3003 Computer Vision | D Y Patil International University, Pune | AY 2026-2027")
            self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
            self.setStrokeColor(HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 46, 558, 46)
            self.restoreState()

    return MemberNumberedCanvas


def get_styles():
    styles = getSampleStyleSheet()
    PRIMARY = HexColor("#0f172a")
    ACCENT_BLUE = HexColor("#2563eb")
    ACCENT_DARK = HexColor("#1e3a8a")
    TEXT_COLOR = HexColor("#334155")
    MUTED = HexColor("#64748b")

    return {
        "PRIMARY": PRIMARY,
        "ACCENT_BLUE": ACCENT_BLUE,
        "ACCENT_DARK": ACCENT_DARK,
        "TEXT_COLOR": TEXT_COLOR,
        "BG_LIGHT": HexColor("#f8fafc"),
        "ALERT_BG": HexColor("#eff6ff"),
        "WARN_BG": HexColor("#fefce8"),
        "WARN_BORDER": HexColor("#eab308"),
        "QA_BG": HexColor("#f1f5f9"),
        "BORDER": HexColor("#cbd5e1"),
        "title": ParagraphStyle(
            "DocTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=17, leading=21, textColor=PRIMARY, spaceAfter=3
        ),
        "subtitle": ParagraphStyle(
            "DocSubtitle", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=14, textColor=ACCENT_BLUE, spaceAfter=4
        ),
        "meta": ParagraphStyle(
            "Meta", parent=styles["Normal"], fontName="Helvetica",
            fontSize=9, leading=13, textColor=MUTED, spaceAfter=8
        ),
        "h1": ParagraphStyle(
            "H1", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=12.5, leading=16, textColor=PRIMARY, spaceBefore=12, spaceAfter=5, keepWithNext=True
        ),
        "h2": ParagraphStyle(
            "H2", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=14, textColor=ACCENT_DARK, spaceBefore=8, spaceAfter=3, keepWithNext=True
        ),
        "body": ParagraphStyle(
            "Body", parent=styles["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=13.5, textColor=TEXT_COLOR, spaceAfter=5
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=styles["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=13.5, textColor=TEXT_COLOR, leftIndent=14, firstLineIndent=-8, spaceAfter=3.5
        ),
        "box_text": ParagraphStyle(
            "BoxText", parent=styles["Normal"], fontName="Helvetica",
            fontSize=9.2, leading=13, textColor=PRIMARY, spaceAfter=2
        ),
        "tbl_hdr": ParagraphStyle(
            "TblHdr", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=11, textColor=HexColor("#ffffff")
        ),
        "tbl_cell": ParagraphStyle(
            "TblCell", parent=styles["Normal"], fontName="Helvetica",
            fontSize=8.5, leading=11.5, textColor=TEXT_COLOR
        ),
    }


def build_callout(st, title_text: str, body_paragraphs: list, bg_hex, border_hex):
    content = [[Paragraph(f"<b>{title_text}</b>", st["box_text"])]]
    for p in body_paragraphs:
        content.append([Paragraph(p, st["box_text"])])
    tbl = Table(content, colWidths=[504])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_hex),
        ("BOX", (0, 0), (-1, -1), 0.75, border_hex),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, border_hex),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 2),
    ]))
    return KeepTogether([tbl, Spacer(1, 6)])


def build_qa_block(st, q_text: str, a_text: str):
    tbl = Table([
        [Paragraph(f"<b>{q_text}</b>", st["box_text"])],
        [Paragraph(f"<b>Answer:</b> {a_text}", st["body"])]
    ], colWidths=[504])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), st["QA_BG"]),
        ("BACKGROUND", (0, 1), (0, 1), HexColor("#ffffff")),
        ("BOX", (0, 0), (-1, -1), 0.6, st["BORDER"]),
        ("LINEBEFORE", (0, 0), (0, -1), 3, st["ACCENT_BLUE"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([tbl, Spacer(1, 6)])


def add_shared_pitch_and_traps(story, st, member_role_line: str):
    story.append(Paragraph("SECTION 1: THE 30-SECOND TEAM PITCH (WHAT EVERYONE MUST KNOW)", st["h1"]))
    story.append(Paragraph(
        "Even though each teammate owns specific files, examiners always start by checking if you understand "
        "the whole project. Memorize these three core points word-for-word in your own voice:",
        st["body"]
    ))
    story.append(Paragraph(
        "- <b>Why Unsupervised Anomaly Detection?</b> Standard classifiers (YOLO, CNNs) need thousands of defective "
        "photos. In real factories, 99.9% of parts are good and defects are unpredictable (scratches, stains, chips). "
        "Our model trains <b>exclusively on good (defect-free) images</b> and flags anything mathematically far from normal.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Core Project Comparison (PatchCore vs. EfficientAD):</b> We implemented <b>PatchCore (CVPR 2022)</b> from scratch "
        "in PyTorch (non-parametric memory bank, 0 training epochs, ~10-15s setup on CPU, slower query at ~2.3-2.6s on CPU) "
        "and compared its accuracy-latency trade-offs against <b>EfficientAD (WACV 2024)</b> (Student-Teacher distillation, "
        "heavy ~70,000-iteration GPU training, ultra-fast &lt;10 ms GPU / &lt;50 ms CPU inference).",
        st["bullet"]
    ))
    story.append(Paragraph(
        f"- <b>Your Role ({member_role_line}) &amp; Verified Demo Results:</b> Tested on MVTec AD <i>bottle</i> "
        "(209 normal train, 83 test images): Normal sample scored <b>1.3007</b> (PASS), broken bottle scored <b>3.2781</b> (DEFECT) "
        "against calibrated threshold <b>2.5000</b> — a clean separation margin of <b>1.9774</b>.",
        st["bullet"]
    ))
    story.append(Spacer(1, 4))

    # Comparison Table
    comp_data = [
        [Paragraph("Metric / Feature", st["tbl_hdr"]),
         Paragraph("PatchCore (CVPR 2022)", st["tbl_hdr"]),
         Paragraph("EfficientAD (WACV 2024)", st["tbl_hdr"])],
        [Paragraph("<b>Core Mechanism</b>", st["tbl_cell"]),
         Paragraph("Memory Bank + Nearest Neighbor Search", st["tbl_cell"]),
         Paragraph("Student-Teacher Distillation + Autoencoder", st["tbl_cell"])],
        [Paragraph("<b>Training Required</b>", st["tbl_cell"]),
         Paragraph("<b>0 epochs</b> (~10-15 sec CPU coreset fit)", st["tbl_cell"]),
         Paragraph("~70,000 iterations (~1-2 hrs per class on GPU)", st["tbl_cell"])],
        [Paragraph("<b>Inference Speed</b>", st["tbl_cell"]),
         Paragraph("~2.3-2.6 sec (CPU) / ~50-150 ms (GPU)", st["tbl_cell"]),
         Paragraph("<b>&lt;50 ms (CPU) / &lt;10 ms (GPU)</b>", st["tbl_cell"])],
        [Paragraph("<b>Published Accuracy</b>", st["tbl_cell"]),
         Paragraph("99.1% Image AUROC / 98.1% Pixel AUROC", st["tbl_cell"]),
         Paragraph("99.1% Image AUROC / 97.8% Pixel AUROC", st["tbl_cell"])],
        [Paragraph("<b>Best Factory Fit</b>", st["tbl_cell"]),
         Paragraph("Low-volume, frequent product swaps", st["tbl_cell"]),
         Paragraph("High-speed lines (&gt;1,000 parts/min)", st["tbl_cell"])],
    ]
    comp_tbl = Table(comp_data, colWidths=[118, 193, 193])
    comp_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), st["PRIMARY"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), st["BG_LIGHT"]]),
        ("GRID", (0, 0), (-1, -1), 0.5, st["BORDER"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(KeepTogether([comp_tbl, Spacer(1, 8)]))


def add_cross_traps_and_commands(story, st):
    story.append(Paragraph("SECTION 4: CROSS-TEAM 'TRAP' QUESTIONS &amp; LIVE DEMO CHEAT SHEET", st["h1"]))
    story.append(Paragraph(
        "Professors often ask these general questions to any random member of the group:",
        st["body"]
    ))
    story.append(build_qa_block(
        st,
        "Trap Q1: Why is your threshold 2.50? Will 2.50 work if we test on screws or carpet?",
        "For MVTec AD 'bottle', good images scored around 1.3007 and defective images around 3.2781, so 2.50 sits cleanly "
        "in the middle of that 1.9774 gap. No, 2.50 is NOT universal across all objects—raw Euclidean feature distances vary "
        "by surface texture, so each new product category requires calibrating the threshold on normal validation samples."
    ))
    story.append(build_qa_block(
        st,
        "Trap Q2: Why does PatchCore take ~2.3 to 2.6 seconds per image in the demo? Isn't that too slow for a factory?",
        "Two reasons: (1) we ran it on an Intel CPU rather than a CUDA GPU, and (2) exact Euclidean distance calculation "
        "between 784 query patches and 1,638 memory vectors uses brute-force tensor broadcasting on CPU. Moving to GPU drops "
        "latency to ~50-150 ms, and using FAISS approximate search or EfficientAD drops it to under 10 ms."
    ))
    story.append(build_qa_block(
        st,
        "Trap Q3: What happens if a bottle or part is rotated by 90 degrees, or has an internal hidden crack?",
        "Our 3x3 average pooling handles slight 1-2 pixel camera shifts, not large 90-degree rotations on structured parts "
        "(rotational data augmentation in the memory bank fixes that). Also, because we use 2D RGB cameras, the model only "
        "sees surface optical defects—internal hidden voids or subsurface cracks require X-ray, ultrasound, or 3D sensors."
    ))
    story.append(build_callout(
        st,
        "LIVE DEMO TERMINAL COMMANDS (PROJECT DIRECTORY: industrial_ad)",
        [
            "- <b>Fast Terminal Verification (proves dataset + PatchCore + SQLite in ~15 sec):</b>  <font face='Courier'>python run_demo.py</font>",
            "- <b>Launch Visual Web Dashboard:</b>  <font face='Courier'>streamlit run app.py</font>",
            "- <b>GitHub Evidence Link:</b>  <font face='Courier'>https://github.com/sawantpratik785-sudo/QualiVision-Industrial-AD</font>"
        ],
        st["WARN_BG"], st["WARN_BORDER"]
    ))


def generate_anvesh_pdf(out_path: str):
    st = get_styles()
    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    story = []

    story.append(Paragraph("TEAMMATE VIVA &amp; TOPIC REVISION GUIDE — ANVESH PATIL", st["title"]))
    story.append(Paragraph(
        "Role: Data Architecture (dataset.py) &amp; EfficientAD Knowledge Distillation Benchmark | PRN: 20240802334",
        st["subtitle"]
    ))
    story.append(Paragraph(
        "Project: Unsupervised Visual Anomaly Detection for Industrial Quality Inspection (PatchCore vs. EfficientAD) | Team: Pratik, Anvesh, Jayesh",
        st["meta"]
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=st["ACCENT_BLUE"], spaceAfter=10))

    add_shared_pitch_and_traps(story, st, "Data Loader &amp; EfficientAD Benchmark")

    story.append(Paragraph("SECTION 2: YOUR TOPICS EXPLAINED SIMPLY (DATASET.PY &amp; EFFICIENTAD)", st["h1"]))

    story.append(Paragraph("1. Why Standard PyTorch Loaders Fail on MVTec AD (dataset.py)", st["h2"]))
    story.append(Paragraph(
        "Normal PyTorch helpers like <i>ImageFolder</i> assume every folder is a simple class name (like cats/ vs. dogs/). "
        "MVTec AD has an asymmetric unsupervised structure built specifically for one-class inspection:",
        st["body"]
    ))
    story.append(Paragraph(
        "- <b>train/good/ (209 images):</b> Contains ONLY defect-free bottles. Zero defect images are used during setup.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>test/ (83 images):</b> Contains 4 subfolders: <i>good</i>, <i>broken_large</i>, <i>broken_small</i>, and <i>contamination</i>.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>ground_truth/&lt;defect&gt;/&lt;name&gt;_mask.png:</b> Black-and-white pixel masks showing exact defect locations for test defects.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "Our custom class <b>MVTecDataset(Dataset)</b> walks <i>train/</i> or <i>test/</i> automatically, assigns label <b>0</b> to "
        "'good' and label <b>1</b> to any defect folder, and automatically pairs each defective test image with its matching "
        "<i>_mask.png</i> file (or creates a blank all-zero tensor mask if the image is 'good').",
        st["body"]
    ))

    story.append(Paragraph("2. Image Preprocessing &amp; The NEAREST Interpolation Rule", st["h2"]))
    story.append(Paragraph(
        "- <b>RGB Image Transform:</b> Every photo is resized to <b>224x224</b>, converted to a tensor (0.0 to 1.0), and normalized "
        "using ImageNet mean <b>[0.485, 0.456, 0.406]</b> and std <b>[0.229, 0.224, 0.225]</b> so it matches the frozen ResNet-18 weights.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Mask Transform (CRITICAL DETAIL):</b> Ground-truth masks are resized with <b>InterpolationMode.NEAREST</b> (never bilinear!) "
        "and thresholded at <b>&gt; 0.5</b>. Bilinear interpolation blends black (0) and white (1) pixels at edges into gray decimals (0.3, 0.7), "
        "which corrupts strict binary pixel labels.",
        st["bullet"]
    ))

    story.append(Paragraph("3. How EfficientAD (WACV 2024) Works — Simple Intuition", st["h2"]))
    story.append(Paragraph(
        "PatchCore gets high accuracy (99.1% AUROC) but is slow on CPU because every query patch searches a 1,638-vector memory bank. "
        "<b>EfficientAD</b> removes the memory bank completely using <b>Student-Teacher Knowledge Distillation</b>:",
        st["body"]
    ))
    story.append(Paragraph(
        "- <b>Teacher Network (Frozen PDN):</b> A compact, ImageNet-pretrained Patch Description Network whose weights never change.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Student Network (Trainable):</b> Has the same architecture as the Teacher, trained via backpropagation <b>only on good images</b> "
        "to copy the Teacher's output feature maps using L2 (Mean Squared Error) loss.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Why It Exposes Defects:</b> On normal surfaces, Student output matches Teacher output (difference is near 0). On an unseen scratch, "
        "the Student has never seen that pattern during training, so it fails to imitate the Teacher -> large difference flags the anomaly!",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Autoencoder Branch:</b> Runs alongside the Student to catch <i>logical/structural anomalies</i> (e.g., a missing bottle cap or wrong label) "
        "that look locally normal in small patches.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Why It Is So Fast:</b> Just one forward pass through the CNN—no nearest-neighbor search—giving <b>&lt;10 ms on GPU</b> and <b>&lt;50 ms on CPU</b>.",
        st["bullet"]
    ))

    story.append(Paragraph("SECTION 3: COUNTER Q&amp;A FOR ANVESH (TOUGH VIVA QUESTIONS)", st["h1"]))
    story.append(build_qa_block(
        st,
        "Q1: Why does MVTecDataset return an all-zero mask tensor for 'good' images instead of None?",
        "PyTorch's DataLoader stacks individual samples into uniform batches like (Batch, 1, 224, 224). Returning None for normal "
        "images inside a mixed test batch would crash PyTorch's default collation function, so returning torch.zeros((1, 224, 224)) "
        "keeps every sample's dictionary shape identical."
    ))
    story.append(build_qa_block(
        st,
        "Q2: Why normalize bottle images using ImageNet mean/std instead of computing the bottle dataset's own mean/std?",
        "Because our ResNet-18 feature extractor is frozen with ImageNet-pretrained weights. Its convolutional filters were "
        "calibrated on ImageNet pixel distributions—changing normalization statistics would misalign early edge and texture activations."
    ))
    story.append(build_qa_block(
        st,
        "Q3: Why is InterpolationMode.NEAREST mandatory when resizing masks?",
        "A ground-truth mask is strictly binary (0 = normal pixel, 1 = defective pixel). Bilinear resizing averages neighboring pixels "
        "and creates blurry fractional values (e.g., 0.42) along defect boundaries, whereas NEAREST copies exact pixel values cleanly."
    ))
    story.append(build_qa_block(
        st,
        "Q4: If EfficientAD runs in under 10 ms and gets the same 99.1% Image AUROC, why would any factory use PatchCore?",
        "Because of training time and product changeovers. EfficientAD requires ~70,000 gradient-descent iterations (1-2 hours on GPU) "
        "for every single SKU. PatchCore needs 0 training epochs and fits a new part in 10-15 seconds on a CPU, making PatchCore far "
        "better for custom or rapidly changing product lines."
    ))
    story.append(build_qa_block(
        st,
        "Q5: In EfficientAD, what stops the Student from just copying the Teacher on defective images too?",
        "Two things: first, the Student only sees good images during training so it never learns defect feature mappings; second, "
        "EfficientAD uses a lightweight Student architecture and hard-feature loss penalties specifically designed so the Student "
        "cannot generalize Teacher responses onto anomalous textures."
    ))
    story.append(build_qa_block(
        st,
        "Q6: Why does EfficientAD need a third Autoencoder branch on top of Student and Teacher?",
        "The Student-Teacher pair looks at small local patches, so it catches local surface flaws (cracks, stains) brilliantly, "
        "but can miss global structural errors (like a missing component or swapped label that looks locally normal). The Autoencoder's "
        "global bottleneck captures full-image structural violations."
    ))

    add_cross_traps_and_commands(story, st)

    CanvasCls = make_canvas_class("AIM3003 CV Viva Guide — Anvesh Patil (20240802334)", "QualiVision Industrial AD")
    doc.build(story, canvasmaker=CanvasCls)


def generate_jayesh_pdf(out_path: str):
    st = get_styles()
    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    story = []

    story.append(Paragraph("TEAMMATE VIVA &amp; TOPIC REVISION GUIDE — JAYESH DESHMUKH", st["title"]))
    story.append(Paragraph(
        "Role: Anomaly Scoring, Gaussian Smoothing, Streamlit QA UI (app.py) &amp; SQLite Logger (db_logger.py) | PRN: 20240802335",
        st["subtitle"]
    ))
    story.append(Paragraph(
        "Project: Unsupervised Visual Anomaly Detection for Industrial Quality Inspection (PatchCore vs. EfficientAD) | Team: Pratik, Anvesh, Jayesh",
        st["meta"]
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=st["ACCENT_BLUE"], spaceAfter=10))

    add_shared_pitch_and_traps(story, st, "Scoring, Streamlit UI &amp; SQLite Audit Trail")

    story.append(Paragraph("SECTION 2: YOUR TOPICS EXPLAINED SIMPLY (SCORING, APP.PY &amp; DB_LOGGER.PY)", st["h1"]))

    story.append(Paragraph("1. How Anomaly Scoring Works During Inference (patchcore.py -> predict)", st["h2"]))
    story.append(Paragraph(
        "When a test photo arrives, Pratik's extractor cuts it into <b>784 query patches</b> (a <b>28x28</b> spatial grid of 384-D vectors). "
        "Your scoring pipeline converts those vectors into a crystal-clear PASS/DEFECT verdict and visual heatmap:",
        st["body"]
    ))
    story.append(Paragraph(
        "- <b>Nearest-Neighbor Distance:</b> Each of the 784 query patches is compared (Euclidean L2 distance) against all <b>1,638 normal vectors</b> "
        "in the memory bank, keeping only its <b>closest match</b> (<i>min_dists</i>). Known normal glass -> tiny distance; unseen crack -> huge distance.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Upsampling:</b> The 784 scores are reshaped back into a <b>28x28</b> grid and bilinearly upsampled to <b>224x224</b> (full image size).",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>2D Gaussian Smoothing (sigma = 4):</b> Raw upsampled grids look blocky and can trigger false alarms from 1-pixel camera noise. "
        "<i>gaussian_filter(anomaly_map, sigma=4)</i> averages out isolated single-pixel noise spikes while keeping real multi-pixel cracks strong.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Max Score &amp; Verdict:</b> Image score = <b>np.max(anomaly_map)</b>. If <i>score &gt;= threshold (2.50)</i> -> <b>DEFECT</b>, else <b>PASS</b>.",
        st["bullet"]
    ))

    story.append(Paragraph("2. Heatmap Visualization &amp; Streamlit Caching (app.py)", st["h2"]))
    story.append(Paragraph(
        "- <b>JET Colormap Alpha Blending:</b> We normalize the smoothed heatmap to 0-255, apply OpenCV's <b>COLORMAP_JET</b> (Blue = normal, "
        "Red/Yellow = high anomaly), convert BGR to RGB, and blend <b>60% original image + 40% heatmap</b> so operators see the flaw over the exact physical part.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>@st.cache_resource:</b> Streamlit normally re-runs the entire Python file top-to-bottom on every button click or slider move. "
        "Wrapping <i>load_model()</i> in <i>@st.cache_resource</i> builds the 1,638-vector coreset <b>only once</b> and keeps it in RAM.",
        st["bullet"]
    ))
    story.append(Paragraph(
        "- <b>Absolute Path Anchoring (BASE_DIR):</b> Using <i>os.path.dirname(os.path.abspath(__file__))</i> guarantees <i>data/</i> and "
        "<i>inspections.db</i> resolve reliably regardless of what folder Streamlit is launched from.",
        st["bullet"]
    ))

    story.append(Paragraph("3. Industrial Traceability with SQLite (db_logger.py)", st["h2"]))
    story.append(Paragraph(
        "Inspired by ISO 9001 and aerospace (GE Aerospace) quality audit standards, every inspected part can be committed to an embedded "
        "<b>SQLite relational database (inspections.db)</b> in table <i>inspection_records</i> logging 8 fields: "
        "<b>timestamp, part_category, model_used, anomaly_score, threshold, verdict, latency_ms,</b> and <b>image_name</b>.",
        st["body"]
    ))

    story.append(Paragraph("SECTION 3: COUNTER Q&amp;A FOR JAYESH (TOUGH VIVA QUESTIONS)", st["h1"]))
    story.append(build_qa_block(
        st,
        "Q1: Why do you use np.max(anomaly_map) instead of np.mean(anomaly_map) to decide PASS or DEFECT?",
        "A real crack or chipped bottle rim might cover only 1-2% of the total image area. If we took the average across the whole image, "
        "the 98% defect-free glass would pull the average down and hide the defect (false negative). Taking the maximum catches a defect "
        "anywhere on the part, no matter how localized it is."
    ))
    story.append(build_qa_block(
        st,
        "Q2: Doesn't Gaussian smoothing (sigma=4) blur away tiny micro-defects?",
        "Slightly, yes—and that is an intentional engineering trade-off. sigma=4 suppresses isolated 1-pixel camera sensor noise so we don't "
        "get false alarms, while real physical cracks spanning several pixels remain strong. For microscopic pinholes, we can tune sigma down to 1 or 2."
    ))
    story.append(build_qa_block(
        st,
        "Q3: On line 222 of app.py, if a bottle is 100% GOOD, why can the heatmap overlay still show some red/yellow regions?",
        "Great observation! Line 222 uses per-image min-max normalization ((map - min) / (max - min)) for visual contrast. Even when the "
        "highest pixel on a good bottle is only 1.30 (well below 2.50 = PASS), min-max stretches that relative peak to 255 (red) for contrast. "
        "In production, normalizing against a fixed global ceiling (e.g., 0 to 5.0) keeps normal bottles completely blue."
    ))
    story.append(build_qa_block(
        st,
        "Q4: What actually happens in app.py if I click the 'EfficientAD (WACV 2024 - Benchmark)' radio button?",
        "To be 100% transparent about our code (app.py lines 146-218): our live interactive dashboard executes our from-scratch PatchCore "
        "model (patchcore_model.predict), while EfficientAD is included in our project as our architectural and quantitative benchmark "
        "(Research Paper Table II) comparing memory-bank search against student-teacher distillation."
    ))
    story.append(build_qa_block(
        st,
        "Q5: Why did you choose SQLite instead of saving logs to a simple CSV file or a heavy MongoDB/PostgreSQL server?",
        "Flat CSV files can get corrupted during concurrent writes and have no strict column types or autoincrement keys. Full database servers "
        "like PostgreSQL add unnecessary network setup on an edge inspection PC. SQLite is zero-configuration, serverless, single-file, and fully "
        "ACID-compliant, guaranteeing reliable audit records."
    ))
    story.append(build_qa_block(
        st,
        "Q6: What does your Streamlit threshold slider prove during a live demo?",
        "It demonstrates human-in-the-loop QA calibration: factory engineers can tighten or relax tolerance dynamically (from 1.0 to 6.0, "
        "default 2.50) and immediately observe the PASS/DEFECT verdict flip without touching a line of code or retraining the model."
    ))

    add_cross_traps_and_commands(story, st)

    CanvasCls = make_canvas_class("AIM3003 CV Viva Guide — Jayesh Deshmukh (20240802335)", "QualiVision Industrial AD")
    doc.build(story, canvasmaker=CanvasCls)


if __name__ == "__main__":
    base = r"C:\Users\Lenovo\.gemini\antigravity\scratch\industrial_ad"
    anvesh_pdf = os.path.join(base, "Anvesh_Patil_Study_and_Viva_Guide.pdf")
    jayesh_pdf = os.path.join(base, "Jayesh_Deshmukh_Study_and_Viva_Guide.pdf")

    generate_anvesh_pdf(anvesh_pdf)
    generate_jayesh_pdf(jayesh_pdf)

    print("Generated:", anvesh_pdf, "| Size:", os.path.getsize(anvesh_pdf), "bytes")
    print("Generated:", jayesh_pdf, "| Size:", os.path.getsize(jayesh_pdf), "bytes")
