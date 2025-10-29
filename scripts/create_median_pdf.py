#!/usr/bin/env python3
"""
Create professional PDF report with median comparison: March 2025 vs All Period
Designed as template for future comparisons (November 2025 daily work)
Focus on medians only, strict business style
"""

import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'output', 'march_2025_median_comparison.pdf')

# Load data
df = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'anki_daily_reviews_honest.csv'))
df['Date'] = pd.to_datetime(df['Date'])

# All period - active days only
all_active = df[df['Total'] > 0].copy()

# March 2025 - active days only
march = df[(df['Date'] >= '2025-03-01') & (df['Date'] <= '2025-03-31')].copy()
march_active = march[march['Total'] > 0].copy()

# Calculate medians
medians = {
    'Total': (all_active['Total'].median(), march_active['Total'].median()),
    'Learning': (all_active['Learning'].median(), march_active['Learning'].median()),
    'Review': (all_active['Review'].median(), march_active['Review'].median()),
    'Relearn': (all_active['Relearn'].median(), march_active['Relearn'].median()),
    'Cheated': (all_active['Cheated'].median(), march_active['Cheated'].median())
}

# Activity metrics
activity = {
    'Total_Days': (len(df), len(march)),
    'Active_Days': (len(all_active), len(march_active)),
    'Activity_Rate': (len(all_active)/len(df)*100, len(march_active)/len(march)*100)
}

# Cheating metrics
cheating = {
    'Clean_Days': ((all_active['Cheated'] == 0).sum(), (march_active['Cheated'] == 0).sum()),
    'Clean_Rate': ((all_active['Cheated'] == 0).sum()/len(all_active)*100,
                   (march_active['Cheated'] == 0).sum()/len(march_active)*100),
    'Avg_Cheated': (all_active['Cheated'].mean(), march_active['Cheated'].mean())
}

# Create PDF
doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=A4,
                        topMargin=2.5*cm, bottomMargin=2.5*cm,
                        leftMargin=2.5*cm, rightMargin=2.5*cm)

elements = []
styles = getSampleStyleSheet()

# Styles
title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=10,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#4a4a4a'),
    spaceAfter=30,
    alignment=TA_CENTER
)

heading_style = ParagraphStyle(
    'Heading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=15,
    spaceBefore=25,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#2a2a2a'),
    spaceAfter=8,
    leading=14
)

# Title
title = Paragraph("ANKI STUDY PERFORMANCE REPORT", title_style)
elements.append(title)

subtitle = Paragraph("Median Analysis: March 2025 vs. Baseline Period<br/>June 2023 - October 2025", subtitle_style)
elements.append(subtitle)

# Executive Summary
elements.append(Paragraph("EXECUTIVE SUMMARY", heading_style))

summary_text = (
    "This report analyzes March 2025 performance against the baseline period (June 2023 - October 2025) "
    "to establish benchmark metrics for future comparison. "
    "Analysis focuses on <b>median values</b> to represent typical daily performance. "
    "<br/><br/>"
    "<b>Note:</b> 'Total' metric = Learning + Review - Cheated (honest work only, excluding relearn to avoid double-counting)."
)
elements.append(Paragraph(summary_text, body_style))
elements.append(Spacer(1, 0.8*cm))

# Activity Overview Table
elements.append(Paragraph("1. ACTIVITY OVERVIEW", heading_style))

activity_data = [
    ['Metric', 'Baseline Period', 'March 2025'],
    ['Total Days', f'{activity["Total_Days"][0]}', f'{activity["Total_Days"][1]}'],
    ['Active Days', f'{activity["Active_Days"][0]}', f'{activity["Active_Days"][1]}'],
    ['Activity Rate', f'{activity["Activity_Rate"][0]:.1f}%', f'{activity["Activity_Rate"][1]:.1f}%'],
]

activity_table = Table(activity_data, colWidths=[5*cm, 5*cm, 5*cm])
activity_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2a2a2a')),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d0d0')),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#34495e')),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))

elements.append(activity_table)
elements.append(Spacer(1, 0.5*cm))

note = Paragraph(
    "<i>Note: Activity Rate is critical for comparing March 2025 (58.1%) with future daily consistency targets.</i>",
    ParagraphStyle('Note', parent=body_style, fontSize=9, textColor=colors.HexColor('#7f8c8d'))
)
elements.append(note)
elements.append(Spacer(1, 1*cm))

# Main Metrics Table
elements.append(Paragraph("2. PERFORMANCE METRICS (Median - Typical Active Day)", heading_style))

table_data = [
    ['Metric', 'Baseline Period', 'March 2025', 'Absolute Diff.', 'Relative Diff.'],
]

metrics = [
    ('Total Cards', 'Total'),
    ('Learning (New)', 'Learning'),
    ('Review (Spaced)', 'Review'),
    ('Relearn (Failed)', 'Relearn'),
]

for label, key in metrics:
    all_val, march_val = medians[key]
    diff = march_val - all_val
    diff_pct = (diff / all_val * 100) if all_val > 0 else 0

    table_data.append([
        label,
        f'{all_val:.1f}',
        f'{march_val:.1f}',
        f'{diff:+.1f}',
        f'{diff_pct:+.0f}%'
    ])

table = Table(table_data, colWidths=[4.5*cm, 3*cm, 3*cm, 3*cm, 2.5*cm])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('TOPPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2a2a2a')),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d0d0')),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
    ('TOPPADDING', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))

elements.append(table)
elements.append(Spacer(1, 1*cm))

# Quality Metrics Table
elements.append(Paragraph("3. QUALITY METRICS (Data Integrity)", heading_style))

quality_data = [
    ['Metric', 'Baseline Period', 'March 2025'],
    ['Clean Days (0 cheated)', f'{cheating["Clean_Days"][0]} ({cheating["Clean_Rate"][0]:.1f}%)',
     f'{cheating["Clean_Days"][1]} ({cheating["Clean_Rate"][1]:.1f}%)'],
    ['Avg Cheated/Day', f'{cheating["Avg_Cheated"][0]:.1f} cards',
     f'{cheating["Avg_Cheated"][1]:.1f} cards'],
    ['Median Cheated', f'{medians["Cheated"][0]:.0f} cards',
     f'{medians["Cheated"][1]:.0f} cards'],
]

quality_table = Table(quality_data, colWidths=[5*cm, 5*cm, 5*cm])
quality_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2a2a2a')),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d0d0')),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#27ae60')),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))

elements.append(quality_table)
elements.append(Spacer(1, 0.5*cm))

quality_note = Paragraph(
    "<i>Median Cheated = 0 for both periods indicates majority of days were clean. "
    "Average is higher due to several high-cheating outlier days.</i>",
    ParagraphStyle('Note', parent=body_style, fontSize=9, textColor=colors.HexColor('#7f8c8d'))
)
elements.append(quality_note)
elements.append(Spacer(1, 1*cm))

# Key Findings
elements.append(Paragraph("4. KEY FINDINGS", heading_style))

findings = [
    f"<b>Intensity:</b> March 2025 typical day = {medians['Total'][1]:.0f} cards vs. "
    f"baseline {medians['Total'][0]:.0f} cards (+{(medians['Total'][1]/medians['Total'][0] - 1)*100:.0f}%).",

    f"<b>Review Focus:</b> Review cards increased from {medians['Review'][0]:.0f} to "
    f"{medians['Review'][1]:.0f} per typical day (+{(medians['Review'][1]/medians['Review'][0] - 1)*100:.0f}%), "
    f"indicating stronger discipline in spaced repetition.",

    f"<b>Retention Challenge:</b> Relearn events rose from {medians['Relearn'][0]:.0f} to "
    f"{medians['Relearn'][1]:.0f} per typical day (+{(medians['Relearn'][1]/medians['Relearn'][0] - 1)*100:.0f}%). "
    f"Higher intensity may impact initial retention quality.",

    f"<b>Data Quality:</b> Average cheating dropped from {cheating['Avg_Cheated'][0]:.1f} to "
    f"{cheating['Avg_Cheated'][1]:.1f} cards/day (-{(1 - cheating['Avg_Cheated'][1]/cheating['Avg_Cheated'][0])*100:.0f}%). "
    f"March 2025 had {cheating['Clean_Rate'][1]:.0f}% clean days vs. {cheating['Clean_Rate'][0]:.0f}% baseline.",

    f"<b>Activity Pattern:</b> March 2025 activity rate = {activity['Activity_Rate'][1]:.1f}% "
    f"(slightly below baseline {activity['Activity_Rate'][0]:.1f}%). "
    f"<b>Critical for future comparison with daily consistency targets.</b>"
]

for i, finding in enumerate(findings, 1):
    p = Paragraph(f"{i}. {finding}", body_style)
    elements.append(p)
    elements.append(Spacer(1, 0.4*cm))

# Benchmark Summary Box
elements.append(Spacer(1, 0.5*cm))
elements.append(Paragraph("5. BENCHMARK SUMMARY", heading_style))

benchmark_text = (
    "<b>Baseline Period (June 2023 - October 2025):</b><br/>"
    f"Typical Day: {medians['Total'][0]:.0f} cards "
    f"({medians['Learning'][0]:.0f}L + {medians['Review'][0]:.0f}R)<br/>"
    f"Activity Rate: {activity['Activity_Rate'][0]:.1f}% ({activity['Active_Days'][0]} active days)<br/>"
    f"Quality: {cheating['Clean_Rate'][0]:.0f}% clean days, avg {cheating['Avg_Cheated'][0]:.1f} cheated/day<br/>"
    f"Relearn Rate: {medians['Relearn'][0]:.0f} errors per typical day<br/><br/>"

    "<b>March 2025 (Best Month):</b><br/>"
    f"Typical Day: {medians['Total'][1]:.0f} cards "
    f"({medians['Learning'][1]:.0f}L + {medians['Review'][1]:.0f}R)<br/>"
    f"Activity Rate: {activity['Activity_Rate'][1]:.1f}% ({activity['Active_Days'][1]} active days)<br/>"
    f"Quality: {cheating['Clean_Rate'][1]:.0f}% clean days, avg {cheating['Avg_Cheated'][1]:.1f} cheated/day<br/>"
    f"Relearn Rate: {medians['Relearn'][1]:.0f} errors per typical day<br/><br/>"

    "<b>Use these benchmarks to compare against November 2025 daily work (100% activity rate target).</b>"
)

benchmark_box = Table([[Paragraph(benchmark_text, body_style)]], colWidths=[16*cm])
benchmark_box.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
    ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3498db')),
    ('TOPPADDING', (0, 0), (-1, -1), 15),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ('LEFTPADDING', (0, 0), (-1, -1), 15),
    ('RIGHTPADDING', (0, 0), (-1, -1), 15),
]))

elements.append(benchmark_box)

# Footer
elements.append(Spacer(1, 1.5*cm))
footer = Paragraph(
    "<i>Report generated: October 29, 2025 | Template for future monthly comparisons</i>",
    ParagraphStyle('Footer', parent=body_style, fontSize=8, textColor=colors.HexColor('#7f8c8d'), alignment=TA_CENTER)
)
elements.append(footer)

# Build PDF
print("Creating professional PDF report...")
doc.build(elements)

print(f"\nPDF created successfully: {OUTPUT_PATH}")
print(f"File size: {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")
print("\nReport focuses on:")
print("  - Median values (typical day)")
print("  - Activity rate (critical for daily consistency)")
print("  - Quality metrics (cheating analysis)")
print("  - Benchmark for future comparison")
