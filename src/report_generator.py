"""
Module — PDF Report Export
Assembles one patient's renal/PK/DDI/dose-adjustment results into a clearly
labeled educational/research decision-support report. NOT a clinical document.
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime


def generate_report(output_path: str, patient_info: dict, renal_result: dict,
                     cat_result: dict, pk_results: dict, ddi_findings: list,
                     adjustment: dict) -> str:
    """
    Builds a PDF report for one patient. All inputs are the same dicts already
    produced by the renal/pk_engine/ddi_engine/dose_adjustment modules — this
    function only formats, it does not recalculate anything.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                             topMargin=0.6 * inch, bottomMargin=0.6 * inch)
    styles = getSampleStyleSheet()
    disclaimer_style = ParagraphStyle(
        "Disclaimer", parent=styles["Normal"], textColor=colors.HexColor("#8B0000"),
        borderColor=colors.HexColor("#8B0000"), borderWidth=1, borderPadding=8,
        backColor=colors.HexColor("#FFF0F0"),
    )
    story = []

    # ---- Header + disclaimer (first thing on the page, not buried) ----
    story.append(Paragraph("DDI + PK Dosing Assistant — Patient Report", styles["Title"]))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                            styles["Normal"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>EDUCATIONAL / RESEARCH DECISION-SUPPORT PROTOTYPE.</b> This report is NOT "
        "a substitute for a physician, pharmacist, official prescribing information, "
        "hospital protocol, or clinical decision-support system. All values require "
        "professional verification before any clinical use.", disclaimer_style))
    story.append(Spacer(1, 16))

    # ---- Patient inputs ----
    story.append(Paragraph("Patient Information", styles["Heading2"]))
    patient_table_data = [[k, str(v)] for k, v in patient_info.items()]
    story.append(_make_table(patient_table_data))
    story.append(Spacer(1, 12))

    # ---- Renal function ----
    story.append(Paragraph("Renal Function", styles["Heading2"]))
    renal_data = [
        ["CrCl (mL/min)", str(renal_result["crcl_ml_min"])],
        ["Category", cat_result["category"]],
        ["Weight basis", renal_result["weight_basis"]],
        ["Reference", renal_result["reference"]],
    ]
    story.append(_make_table(renal_data))
    story.append(Spacer(1, 12))

    # ---- PK calculations, per drug ----
    story.append(Paragraph("Pharmacokinetic Calculations", styles["Heading2"]))
    for drug, result in pk_results.items():
        story.append(Paragraph(f"<b>{drug}</b>", styles["Heading3"]))
        pk_data = [[k, str(v)] for k, v in result.items() if k != "reference"]
        story.append(_make_table(pk_data))
        story.append(Paragraph(f"<i>Source: {result['reference']}</i>", styles["Normal"]))
        story.append(Spacer(1, 8))

    # ---- DDI findings ----
    story.append(Paragraph("Drug-Drug Interaction Assessment", styles["Heading2"]))
    if not ddi_findings:
        story.append(Paragraph("No drug pairs assessed (fewer than 2 drugs selected).",
                                styles["Normal"]))
    for finding in ddi_findings:
        if finding["pair_found_in_kb"]:
            story.append(Paragraph(
                f"<b>{finding['drug_a']} + {finding['drug_b']}</b> — "
                f"Severity: <b>{finding['severity']}</b> ({finding['interaction_category']})<br/>"
                f"{finding['effect']}<br/>"
                f"Recommendation: {finding['clinical_recommendation']}<br/>"
                f"<i>Source: {finding['reference']}</i>", styles["Normal"]))
        else:
            story.append(Paragraph(
                f"<b>{finding['drug_a']} + {finding['drug_b']}</b> — not in sourced "
                f"knowledge base. {finding['note']}", styles["Normal"]))
        story.append(Spacer(1, 6))

    # ---- Dose adjustment / clinical interpretation ----
    story.append(Paragraph("Dose Adjustment Assessment", styles["Heading2"]))
    if adjustment["adjustment_indicated"]:
        story.append(Paragraph("<b>Adjustment may be indicated:</b>", styles["Normal"]))
        for reason in adjustment["reasons"]:
            story.append(Paragraph(f"• {reason}", styles["Normal"]))
    else:
        story.append(Paragraph(
            "No adjustment triggers identified from renal/DDI/hepatic factors assessed.",
            styles["Normal"]))
    story.append(Paragraph(f"<i>{adjustment['note']}</i>", styles["Normal"]))
    story.append(Spacer(1, 16))

    # ---- References ----
    story.append(Paragraph("References", styles["Heading2"]))
    refs = [
        "Bauer LA. Applied Clinical Pharmacokinetics, 2nd ed. McGraw-Hill; 2008.",
        "Winter M (Beringer). Basic Clinical Pharmacokinetics, 6th ed.",
        "Rybak MJ et al. Am J Health-Syst Pharm. 2020;77(11):835-864.",
        "Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41.",
        "FDA Guidance for Industry, Pharmacokinetics in Patients with Impaired Renal Function.",
    ]
    for ref in refs:
        story.append(Paragraph(f"• {ref}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # ---- Final disclaimer, repeated at the end (not just the top) ----
    story.append(Paragraph(
        "This report was generated by an educational/research prototype tool. It has "
        "not been clinically validated for patient care use. Do not use for actual "
        "treatment decisions without independent verification by a qualified "
        "healthcare professional.", disclaimer_style))

    doc.build(story)
    return output_path


def _make_table(data: list) -> Table:
    t = Table(data, colWidths=[180, 320])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F0F0")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t
