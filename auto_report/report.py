# ------------------------------------------------------------
# report.py
# Handles all report generation for AutoReport AI.
#
# Responsibilities:
#   1. Generate a clean, text-only PDF report containing:
#        - Dataset summary
#        - AI-generated insights
#
#   2. Generate a visual-only PPTX report containing:
#        - Correlation heatmap
#        - Distribution charts for numeric features
#
#   3. Ensure visual consistency across both formats:
#        - No text overflow in slides
#        - Clean layout without unwanted bullets
#        - Auto-scaling of charts and slide content
#
#   4. Provide utilities for:
#        - Cleaning and formatting insight text
#        - Dynamically constructing slides
#        - Rendering matplotlib/seaborn plots to in-memory images
#
# Purpose:
#   This module is the final stage of the analytics pipeline. It converts
#   processed dataset statistics, AI insights, and generated visualizations
#   into polished, presentation-ready reports for end users.
#
# Output:
#   /output/<dataset_name>/
#       ├── <dataset>_summary.pdf   (summary + insights)
#       └── <dataset>_graphs.pptx   (heatmap + histograms)
#
# ------------------------------------------------------------

import os
import io
import matplotlib.pyplot as plt
import seaborn as sns

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.oxml.xmlchemy import OxmlElement

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_LEFT



# TEXT CLEANING

def clean_text(line: str):
    return (
        line.replace("•", "")
            .replace("*", "")
            .replace("**", "")
            .strip()
    )


def disable_bullets(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    buNone = OxmlElement("a:buNone")
    pPr.append(buNone)



# SUMMARY + INSIGHT FORMATTERS

def format_summary(summary_dict):
    lines = [
        f"Total Rows: {summary_dict.get('rows')}",
        f"Total Columns: {summary_dict.get('columns')}",
        "Missing Values:",
    ]
    for col, count in summary_dict.get("missing_values", {}).items():
        lines.append(f"{col}: {count}")
    return lines


def format_insights(text):
    cleaned = []
    for line in text.split("\n"):
        line = clean_text(line)
        if line:
            cleaned.append(line)
    return cleaned


# PDF REPORT → ONLY TEXT (NO IMAGES)

def create_pdf(summary, insights, folder_path, filename="summary_report.pdf"):
    pdf_path = os.path.join(folder_path, filename)
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "BodyClean",
        parent=styles["BodyText"],
        fontSize=12,
        leading=16,
        alignment=TA_LEFT,
    )

    story = []

    # Title
    story.append(Paragraph("AI Summary Report", styles["Title"]))
    story.append(Spacer(1, 16))

    # Summary Section
    story.append(Paragraph("Dataset Summary", styles["Heading2"]))
    for line in format_summary(summary):
        story.append(Paragraph(clean_text(line), body_style))
    story.append(Spacer(1, 20))

    # Insights Section
    story.append(Paragraph("AI Insights", styles["Heading2"]))
    for line in format_insights(insights):
        story.append(Paragraph(clean_text(line), body_style))
    story.append(Spacer(1, 20))

    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    pdf.build(story)

    return pdf_path


# PPTX REPORT → ONLY GRAPHS

def create_ppt(plot_images, heatmap, folder_path, filename="graph_report.pptx"):
    prs = Presentation()
    ppt_path = os.path.join(folder_path, filename)

    BLANK = prs.slide_layouts[6]

    # Title Slide
    slide = prs.slides.add_slide(BLANK)
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(1.5))
    title_tf = title_box.text_frame
    title_tf.text = "Graphical Analysis Report"
    title_tf.paragraphs[0].font.size = Pt(48)

    # Heatmap Slide
    if heatmap:
        slide = prs.slides.add_slide(BLANK)
        tbox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(1))
        ttf = tbox.text_frame
        ttf.text = "Correlation Heatmap"
        ttf.paragraphs[0].font.size = Pt(36)

        slide.shapes.add_picture(heatmap, Inches(1), Inches(1.4), width=Inches(7))

    # Histogram Slides
    for col, img in plot_images:
        slide = prs.slides.add_slide(BLANK)
        tbox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(1))
        ttf = tbox.text_frame
        ttf.text = f"Distribution: {col}"
        ttf.paragraphs[0].font.size = Pt(36)

        slide.shapes.add_picture(img, Inches(1), Inches(1.4), width=Inches(7))

    prs.save(ppt_path)
    return ppt_path
