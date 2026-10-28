import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

class IndividualVivaNumberedCanvas(canvas.Canvas):
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
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(HexColor("#64748b"))
        if self._pageNumber > 1:
            self.drawString(54, 750, "AIM3003 Computer Vision — Individual Viva Defense & Implementation Scripts")
            self.drawRightString(558, 750, "Pratik | Anvesh | Jayesh")
            self.setStrokeColor(HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        self.setFont("Helvetica", 8)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_text)
        self.drawString(54, 34, "D Y Patil International University | Dept. of Computer Science & Engineering | AY 2026-2027")
        self.setStrokeColor(HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_individual_viva_pdf():
    pdf_path = r"C:\Users\Lenovo\.gemini\antigravity\scratch\industrial_ad\Individual_Viva_Defense_Scripts.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    PRIMARY = HexColor("#0f172a")     # Slate 900
    ACCENT_BLUE = HexColor("#2563eb") # Royal Blue
    ACCENT_CYAN = HexColor("#0284c7") # Deep Cyan
    TEXT_COLOR = HexColor("#334155")  # Slate 700
    BG_LIGHT = HexColor("#f8fafc")    # Slate 50
    BORDER_COLOR = HexColor("#cbd5e1")
    ALERT_BG = HexColor("#eff6ff")    # Light Blue
    CODE_BG = HexColor("#f1f5f9")     # Slate 100

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=ACCENT_BLUE,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=ACCENT_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_COLOR,
        spaceAfter=4
    )

    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=HexColor("#1e293b"),
        backColor=ALERT_BG,
        borderColor=ACCENT_BLUE,
        borderWidth=0.8,
        borderPadding=4,
        spaceBefore=2,
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=HexColor("#0f172a"),
        backColor=CODE_BG,
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=2,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=HexColor("#ffffff")
    )

    table_body = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=TEXT_COLOR
    )

    table_body_bold = ParagraphStyle(
        'TableBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=PRIMARY
    )

    story = []

    # Title Banner
    story.append(Paragraph("Individual Viva Defense & Code Implementation Master Scripts", title_style))
    story.append(Paragraph("Task-by-Task Defense Scripts for Pratik Sawant, Anvesh Patil, and Jayesh Deshmukh", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_BLUE, spaceAfter=6))

    # Summary Ownership Table
    summary_data = [
        [Paragraph("Student Name & Roll No.", table_header), Paragraph("Assigned Implementation Tasks", table_header), Paragraph("Code Files Owned", table_header), Paragraph("Core Viva Defense Topics", table_header)],
        [
            Paragraph("<b>Pratik Sawant</b><br/>20240802324", table_body_bold),
            Paragraph("• Task O2-T1: Multi-scale PyTorch layer hooks<br/>• Task O2-T2: 99% greedy coreset subsampling", table_body),
            Paragraph("<code>patchcore.py</code><br/>(Core Algorithmic Engine)", table_body),
            Paragraph("Layer 2 & 3 rationale, 3x3 local pooling, Johnson-Lindenstrauss lemma, Min-Max Greedy k-Center math.", table_body)
        ],
        [
            Paragraph("<b>Anvesh Patil</b><br/>20240802334", table_body_bold),
            Paragraph("• Task O1-T1: MVTec dataset & mask pipeline<br/>• Task O4-T1: EfficientAD distillation framework", table_body),
            Paragraph("<code>dataset.py</code> & EfficientAD Benchmark", table_body),
            Paragraph("MVTec AD directory hierarchy, nearest-neighbor mask interpolation, ImageNet normalization, Student-Teacher distillation.", table_body)
        ],
        [
            Paragraph("<b>Jayesh Deshmukh</b><br/>20240802335", table_body_bold),
            Paragraph("• Task O3-T1: Nearest-neighbor scoring & smoothing<br/>• Task O5-T1: Streamlit UI & SQLite audit logging", table_body),
            Paragraph("<code>app.py</code>, <code>db_logger.py</code>, <code>predict()</code>", table_body),
            Paragraph("Euclidean distance scoring, 2D Gaussian filter (sigma=4), JET colormap alpha blending, SQLite ACID traceability.", table_body)
        ]
    ]

    t_summary = Table(summary_data, colWidths=[110, 140, 110, 144], repeatRows=1)
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 3.5)
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 8))

    # ========================================================
    # PRATIK SAWANT SECTION
    # ========================================================
    story.append(Paragraph("1. Pratik Sawant (Tasks O2-T1 & O2-T2) — Algorithmic Engine", h1_style))
    story.append(Paragraph("<b>Pratik's 90-Second Opening Verbal Pitch:</b>", h2_style))
    story.append(Paragraph(
        '"Good morning respected panel. In our project, my core responsibility was the algorithmic engine of PatchCore in patchcore.py. '
        'For task O2-T1, I implemented multi-scale patch feature extraction from scratch using PyTorch forward hooks. Rather than taking the final classification layer—which discards spatial information—I intercepted intermediate representations from layer2 and layer3 of ResNet-18, applying a 3x3 stride-1 average pooling layer to incorporate local spatial context into every patch. '
        'For task O2-T2, extracting patches across 209 normal training bottles generated 163,856 high-dimensional vectors (each 384-D). Storing all of them causes massive memory overhead and query latency. To solve this, I implemented dimensionality reduction using the Johnson-Lindenstrauss lemma down to 128 dimensions, followed by the Min-Max Greedy k-Center coreset algorithm. This compressed our memory bank by 99%—from 163,856 down to just 1,638 representative vectors—with virtually zero loss in detection accuracy."',
        quote_style
    ))
    story.append(Paragraph("<b>Pratik's Code Walkthrough Lines to Point to:</b>", h2_style))
    story.append(Paragraph("• <b>PyTorch Forward Hooks:</b> <code>self.backbone.layer2.register_forward_hook(...)</code> intercepts intermediate activations without breaking forward inference.<br/>"
                           "• <b>Spatial Aggregation:</b> <code>avg_pool = nn.AvgPool2d(3, stride=1, padding=1)</code> pools 3x3 patch neighbors for vibration invariance; bilinearly upsamples layer3 to match layer2, concatenating into 384-D patch tokens.<br/>"
                           "• <b>Greedy k-Center:</b> <code>_k_center_greedy()</code> iteratively selects the sample whose minimum distance to existing centers is maximum (<code>np.argmax(dist_to_centers)</code>).", body_style))
    story.append(Paragraph("<b>Pratik's Key Viva Defense Q&A:</b>", h2_style))
    story.append(Paragraph("<b>Q: Why didn't you use layer4?</b><br/>"
                           "<b>Answer:</b> Layer 4 has 32x downsampling (224x224 becomes 7x7). The receptive field is too broad, destroying spatial localization for 2mm micro-cracks. Layer 4 is also over-specialized to ImageNet classification categories. Layers 2 and 3 strike the optimal Goldilocks balance.", body_style))
    story.append(Paragraph("<b>Q: What is the Johnson-Lindenstrauss guarantee?</b><br/>"
                           "<b>Answer:</b> It mathematically proves that points in high dimensions can be linearly projected into a lower dimension while preserving pairwise Euclidean distances within (1 +/- epsilon). Projecting from 384-D to 128-D cuts distance operations by 66% with negligible metric distortion.", body_style))

    # ========================================================
    # ANVESH PATIL SECTION
    # ========================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Anvesh Patil (Tasks O1-T1 & O4-T1) — Data & Distillation", h1_style))
    story.append(Paragraph("<b>Anvesh's 90-Second Opening Verbal Pitch:</b>", h2_style))
    story.append(Paragraph(
        '"Good morning respected faculty. My primary responsibilities covered dataset architecture engineering in dataset.py and the EfficientAD distillation comparison framework for task O4-T1. '
        'For task O1-T1, the standard torchvision ImageFolder class cannot handle MVTec AD because the directory structure is non-standard: test images are grouped by defect types, while ground-truth pixel masks are stored in a parallel directory tree. I wrote dataset.py from scratch to automatically pair every defective test image with its corresponding 1-channel binary mask, while applying ImageNet normalization and nearest-neighbor mask resizing. '
        'For task O4-T1, I analyzed and benchmarked EfficientAD. While PatchCore is a memory-bank method with zero training epochs, its query latency is high. EfficientAD solves this by using a pre-trained Teacher Network and training a Student Network to mimic the Teacher on normal images. I configured the 5-class evaluation pipeline (bottle, cable, capsule, metal_nut, transistor) to measure the trade-off between PatchCore\'s memory lookups and EfficientAD\'s sub-10ms forward passes."',
        quote_style
    ))
    story.append(Paragraph("<b>Anvesh's Code Walkthrough Lines to Point to:</b>", h2_style))
    story.append(Paragraph("• <b>Ground Truth Mask Pairing:</b> <code>mask_path = os.path.join(root, 'ground_truth', defect, f'{name}_mask.png')</code> maps defective test images to 1-channel binary segmentation ground-truth masks.<br/>"
                           "• <b>Nearest-Neighbor Mask Transform:</b> <code>Resize((224, 224), interpolation=InterpolationMode.NEAREST)</code> preserves strict integer 0/1 binary values without bilinear edge blur.<br/>"
                           "• <b>ImageNet Normalization:</b> <code>mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]</code> ensures input tensors match the channel distribution of pre-trained convolutional filters.", body_style))
    story.append(Paragraph("<b>Anvesh's Key Viva Defense Q&A:</b>", h2_style))
    story.append(Paragraph("<b>Q: How does EfficientAD detect anomalies without a memory bank?</b><br/>"
                           "<b>Answer:</b> Through knowledge distillation. The Teacher is pre-trained and frozen. The Student is trained strictly on normal images to predict the Teacher's output. When normal parts pass, Student matches Teacher (difference ~ 0). When a crack appears, the Student fails to mimic the Teacher (high difference flags defect in a single forward pass).", body_style))
    story.append(Paragraph("<b>Q: Why train EfficientAD on only 5 classes instead of all 15?</b><br/>"
                           "<b>Answer:</b> PatchCore has 0 training epochs (~15s per class). EfficientAD requires ~70,000 backprop iterations per class (over 1M iterations total). Benchmarking 5 representative object and texture classes provides complete empirical trade-off data within our 12-week compute budget.", body_style))

    # ========================================================
    # JAYESH DESHMUKH SECTION
    # ========================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("3. Jayesh Deshmukh (Tasks O3-T1 & O5-T1) — Scoring & Deployment", h1_style))
    story.append(Paragraph("<b>Jayesh's 90-Second Opening Verbal Pitch:</b>", h2_style))
    story.append(Paragraph(
        '"Good morning respected panel. My focus in this project was the inference scoring pipeline for task O3-T1 and the complete deployment architecture for task O5-T1. '
        'For task O3-T1, I implemented the nearest-neighbor distance computation in patchcore.py. For every query patch in a test image, my code computes the Euclidean distance to the nearest patch in Pratik\'s memory bank. I then interpolate this distance grid back to the original 224x224 resolution and apply a 2D Gaussian filter (sigma = 4) using SciPy. This eliminates high-frequency noise spikes and produces smooth, contiguous anomaly heatmaps. On our test run, defective bottles scored 3.28 while normal bottles scored 1.30, providing a clean 1.98 decision margin. '
        'For task O5-T1, I built our interactive Streamlit application (app.py) and integrated an ACID-compliant SQLite audit trail (db_logger.py) following GE Aerospace exception logging standards. This allows factory operators to inspect parts, view live JET heatmap overlays, adjust decision thresholds, and permanently record inspection events for ISO 9001 quality audits."',
        quote_style
    ))
    story.append(Paragraph("<b>Jayesh's Code Walkthrough Lines to Point to:</b>", h2_style))
    story.append(Paragraph("• <b>Nearest-Neighbor Distance:</b> <code>dists = torch.norm(patches.unsqueeze(1) - memory_bank.unsqueeze(0), p=2, dim=2)</code> computes minimum Euclidean distances to the normal coreset.<br/>"
                           "• <b>2D Gaussian Smoothing:</b> <code>gaussian_filter(anomaly_map, sigma=4)</code> smooths coarse 28x28 distance spikes into continuous defect regions; <code>image_score = float(np.max(anomaly_map))</code> extracts image verdict.<br/>"
                           "• <b>SQLite Audit Logger:</b> <code>db_logger.py</code> inserts timestamp, part category, model, raw score, threshold, verdict, latency, and image name into <code>inspections.db</code>.<br/>"
                           "• <b>Streamlit JET Alpha Blending:</b> <code>overlay = np.uint8(0.6 * img_np + 0.4 * heatmap_color)</code> renders the operator visualization in <code>app.py</code>.", body_style))
    story.append(Paragraph("<b>Jayesh's Key Viva Defense Q&A:</b>", h2_style))
    story.append(Paragraph("<b>Q: Why apply a Gaussian filter?</b><br/>"
                           "<b>Answer:</b> Raw nearest-neighbor patch scores exist on a coarse 28x28 grid. Bilinear upsampling alone leaves blocky artifacts and single-pixel false alarms caused by sensor noise. A 2D Gaussian filter (sigma = 4) smooths noise spikes into physical defect contours.", body_style))
    story.append(Paragraph("<b>Q: Why use SQLite instead of a flat CSV or MongoDB?</b><br/>"
                           "<b>Answer:</b> In manufacturing lines, multiple inspection threads write simultaneously. A flat CSV lacks ACID transactions and corrupts during concurrent writes. MongoDB introduces network latency and server overhead. SQLite is serverless, zero-configuration, ACID-compliant, and embeds directly into industrial edge inspection terminals.", body_style))

    doc.build(story, canvasmaker=IndividualVivaNumberedCanvas)
    print("Individual Viva Defense Scripts PDF generated at:", pdf_path)

if __name__ == "__main__":
    build_individual_viva_pdf()
