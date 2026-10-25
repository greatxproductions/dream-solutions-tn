#!/usr/bin/env python3
"""Branded Signature Clean-Air System proposal PDF — DSTN navy/cyan theme."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY   = HexColor("#0c1219")
CYAN   = HexColor("#00E5FF")
WHITE  = HexColor("#ffffff")
MUTED  = HexColor("#a9b8c7")
CHROME = HexColor("#eef3f7")
DARK2  = HexColor("#101b26")

SHIELD = "/Users/greatxproductions/projects/dream-solutions-tn/public/brand/shield-emblem.png"
OUT    = "/Users/greatxproductions/wiki/concepts/radonwell-mansion-proposal.pdf"

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    # subtle top glow band
    canvas.setFillColor(DARK2)
    canvas.rect(0, letter[1] - 1.55 * inch, letter[0], 1.55 * inch, fill=1, stroke=0)
    # shield + wordmark
    try:
        canvas.drawImage(SHIELD, 0.7 * inch, letter[1] - 1.35 * inch,
                         width=0.62 * inch, height=0.62 * inch, mask='auto')
    except Exception:
        pass
    canvas.setFillColor(CHROME)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(1.45 * inch, letter[1] - 0.72 * inch, "DREAM SOLUTIONS TENNESSEE")
    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(1.45 * inch, letter[1] - 0.97 * inch, "PRESCRIBING CLEAN AIR FOR YOUR HOME")
    # footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(0.7 * inch, 0.5 * inch,
                      "Dream Solutions Tennessee  ·  NRPP-certified  ·  Licensed  ·  Insured")
    canvas.drawRightString(letter[0] - 0.7 * inch, 0.5 * inch, "Private & Confidential")
    canvas.restoreState()

doc = BaseDocTemplate(
    OUT, pagesize=letter,
    leftMargin=0.7 * inch, rightMargin=0.7 * inch,
    topMargin=1.75 * inch, bottomMargin=0.85 * inch,
    title="Signature Clean-Air System Proposal",
    author="Dream Solutions Tennessee",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
doc.addPageTemplates([PageTemplate(id="all", frames=frame, onPage=on_page)])

title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=25,
                       textColor=WHITE, leading=30, spaceAfter=3)
subtitle = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11.5,
                          textColor=MUTED, leading=15, spaceAfter=14)
meta = ParagraphStyle("meta", fontName="Helvetica", fontSize=10,
                      textColor=MUTED, leading=15)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13,
                    textColor=CYAN, leading=16, spaceBefore=18, spaceAfter=7)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=10.5,
                      textColor=WHITE, leading=16, spaceAfter=5)
li = ParagraphStyle("li", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=4)
big = ParagraphStyle("big", fontName="Helvetica-Bold", fontSize=30,
                     textColor=CYAN, leading=34, alignment=TA_CENTER, spaceBefore=6)
term = ParagraphStyle("term", fontName="Helvetica", fontSize=10.5,
                      textColor=MUTED, leading=15, alignment=TA_CENTER, spaceAfter=2)
sig = ParagraphStyle("sig", parent=body, fontSize=10, textColor=WHITE, leading=20)

def rule():
    return HRFlowable(width="100%", thickness=0.7, color=CYAN,
                      spaceBefore=4, spaceAfter=4)

story = []
story.append(Paragraph("Signature Clean-Air System", title))
story.append(Paragraph("A private proposal for your new residence", subtitle))
story.append(Paragraph("Prepared for: <b>[Client Name]</b><br/>Project: [Residence]"
                       "<br/>Date: October 23, 2026", meta))
story.append(Spacer(1, 6))
story.append(rule())

story.append(Paragraph("The Idea", h2))
story.append(Paragraph(
    "Your home is the largest investment your family will ever make. The air inside it "
    "should be held to the same standard as everything else you build — <b>the best "
    "available.</b> This proposal specs the best-in-class radon and air-quality system: "
    "installed to be invisible, <b>guaranteed for life</b>, and monitored continuously so "
    "you never have to think about it.", body))

story.append(Paragraph("What's Included — The Signature Package", h2))
items = [
    "<b>RadonWell® Source Mitigation</b> — a patented sub-soil system that removes radon, soil gases, VOCs, and moisture at the source, before they enter your home. Multiple wells sized to your home's footprint.",
    "<b>Full Encapsulation</b> — reinforced 20-mil vapor barrier, sealed seams, across the entire crawlspace and basement.",
    "<b>Commercial Dehumidification</b> — engineered to hold the space bone-dry.",
    "<b>Whole-Home Air Purification (ERV)</b> — continuous filtered fresh-air exchange.",
    "<b>Multi-Zone Smart Monitoring</b> — continuous radon + air-quality readings on a live dashboard, with instant alerts to your phone. <i>Flagship Airthings View Plus or smart Ecosense EcoQube monitors.</i>",
    "<b>Invisible Installation</b> — every run concealed, every finish matched to your build. No visible pipe, no exposed equipment.",
    "<b>Certification</b> — pre- and post-installation testing by NRPP-certified technicians, with a written report.",
]
for i, t in enumerate(items, 1):
    story.append(Paragraph(f"{i}. {t}", li))

story.append(Paragraph("The Guarantee — For Life", h2))
for t in [
    "<b>Lifetime transferable warranty</b> on the entire system — it follows the house when it sells.",
    "<b>Radon guaranteed below the EPA action level (4.0 pCi/L)</b> — typically reduced to under 2.0 pCi/L — verified in writing after installation.",
    "<b>Transferable:</b> the warranty passes to any future owner, protecting your home's resale value.",
]:
    story.append(Paragraph(f"• {t}", li))

story.append(Paragraph("Continuous Care — The Monitoring Plan", h2))
story.append(Paragraph(
    "The system doesn't end at installation. Your home stays monitored, and we return "
    "annually to re-test and re-certify.", body))
for t in [
    "Live multi-zone dashboard + phone alerts",
    "Annual re-test + re-certification report",
    "Priority same-day service",
    "<b>$599/year</b> — less than $1.65 a day for continuous peace of mind",
]:
    story.append(Paragraph(f"• {t}", li))

story.append(Paragraph("The Investment", h2))
story.append(Spacer(1, 2))
story.append(Paragraph("$30,000 – $35,000", big))
story.append(Paragraph("complete · installed · certified · guaranteed for life", term))
story.append(Spacer(1, 6))
story.append(Paragraph("50% to schedule · 50% on completion", term))
story.append(Spacer(1, 4))
story.append(Paragraph("Base — the main residence, as scoped above.", term))
story.append(Spacer(1, 10))
story.append(Paragraph("Additional Structures on the Property", h2))
story.append(Paragraph("• <b>Pool house</b> — <b>+$4,500</b> — source mitigation + monitoring zone.", li))
story.append(Paragraph("• <b>In-law suite / ADU</b> — <b>+$5,500</b> — full secondary system + monitoring zone.", li))
story.append(Paragraph("The final investment adjusts to the structures on your property.", body))

story.append(Spacer(1, 18))
story.append(rule())
story.append(Paragraph("Acceptance", h2))
story.append(Paragraph("Client: ______________________________&nbsp;&nbsp;&nbsp;&nbsp;"
                       "Date: ____________", sig))
story.append(Spacer(1, 4))
story.append(Paragraph("[Contact] · [Phone]", sig))

doc.build(story)
print("WROTE", OUT)
