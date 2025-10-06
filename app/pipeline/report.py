import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup


def extract_basic_info_from_html(html_path: str) -> dict:
    """Extract a few summary statistics from the ydata HTML report to include in a short PDF summary."""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    summary = {}
    # Try to extract rows/columns from title block or meta - fallbacks used if not found
    # This is heuristic and should be adapted to the version of ydata_profiling used.
    try:
        # find small summary stats
        stats = soup.find_all(class_="item")
        # fallback: not guaranteed — we'll put placeholders
        summary["Remarque"] = "Résumé automatique — voir rapport HTML pour les détails."
    except Exception:
        summary["Remarque"] = "Impossible d'extraire les statistiques."

    return summary


def generate_summary_pdf(html_report_path: str, out_pdf_path: str):
    stats = extract_basic_info_from_html(html_report_path)

    doc = SimpleDocTemplate(out_pdf_path)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("DataAudit.io — Résumé du rapport", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Ce document contient un bref résumé automatique du rapport généré.", styles["Normal"]))
    elements.append(Spacer(1, 12))

    for k, v in stats.items():
        elements.append(Paragraph(f"<b>{k}:</b> {v}", styles["BodyText"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    return out_pdf_path