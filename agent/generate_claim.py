"""
SurplusRecoveryPro - Claim Package Generator
Generates a complete PDF claim package for a surplus funds case.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import uuid


def generate_claim_package(case_data, claimant_data, output_path=None):
    if not output_path:
        package_id = str(uuid.uuid4())[:8].upper()
        output_path = f"/tmp/claim_package_{package_id}.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=16, fontName='Helvetica-Bold', spaceAfter=12, alignment=TA_CENTER)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading1'], fontSize=13, fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=8, textColor=colors.HexColor('#1a365d'))
    subheading_style = ParagraphStyle('CustomSubHeading', parent=styles['Heading2'], fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6)
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, fontName='Helvetica', spaceAfter=6, leading=14)
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=10, fontName='Helvetica', spaceAfter=8, leading=16, alignment=TA_JUSTIFY)
    center_style = ParagraphStyle('Center', parent=styles['Normal'], fontSize=10, fontName='Helvetica', alignment=TA_CENTER, spaceAfter=6)

    today = datetime.now().strftime("%B %d, %Y")
    county = case_data.get('county', 'Unknown')
    property_address = case_data.get('property_address', 'Unknown')
    owner_name = case_data.get('owner_name', 'Unknown')
    surplus_amount = case_data.get('surplus_amount', 0)
    parcel_id = case_data.get('parcel_id', 'N/A')
    sale_date = case_data.get('sale_date', 'N/A')
    case_number = case_data.get('case_number', 'N/A')
    claimant_name = claimant_data.get('claimant_name', '')
    claimant_address = claimant_data.get('claimant_address', '')
    claimant_email = claimant_data.get('claimant_email', '')
    claimant_phone = claimant_data.get('claimant_phone', '')
    claimant_type = claimant_data.get('claimant_type', 'owner').title()

    story = []

    # PAGE 1: COVER LETTER
    story.append(Paragraph("SURPLUS RECOVERY CLAIM PACKAGE", title_style))
    story.append(Paragraph(f"{county} County, Georgia", center_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d')))
    story.append(Spacer(1, 20))
    story.append(Paragraph(claimant_name, normal_style))
    story.append(Paragraph(claimant_address, normal_style))
    story.append(Paragraph(claimant_email, normal_style))
    story.append(Paragraph(claimant_phone, normal_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(today, normal_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"{county} County Tax Commissioner", normal_style))
    story.append(Paragraph(f"{county} County, Georgia", normal_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"<b>RE: Claim for Surplus Funds — {property_address}</b>", normal_style))
    story.append(Paragraph(f"<b>Parcel ID:</b> {parcel_id} | <b>Sale Date:</b> {sale_date} | <b>Estimated Surplus:</b> ${surplus_amount:,.2f}", normal_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Dear Tax Commissioner,", normal_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"I, {claimant_name}, am writing to formally claim the surplus funds generated from the tax sale of the above-referenced property located at {property_address}, {county} County, Georgia.", body_style))
    story.append(Paragraph(f"I am submitting this claim as the <b>{claimant_type}</b> of the above property. Enclosed with this letter you will find the required supporting documentation including an Affidavit of Claim and Motion for Disbursement of Funds.", body_style))
    story.append(Paragraph(f"I respectfully request that the surplus funds in the amount of <b>${surplus_amount:,.2f}</b> be disbursed to me at the address listed above. Please contact me at {claimant_email} or {claimant_phone} if you require any additional documentation.", body_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Respectfully submitted,", normal_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("_______________________________", normal_style))
    story.append(Paragraph(claimant_name, normal_style))
    story.append(Paragraph(f"Claimant ({claimant_type})", normal_style))
    story.append(PageBreak())

    # PAGE 2: AFFIDAVIT
    story.append(Paragraph("AFFIDAVIT OF CLAIM FOR SURPLUS FUNDS", title_style))
    story.append(Paragraph(f"State of Georgia, {county} County", center_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d')))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"I, {claimant_name}, being duly sworn, depose and state as follows:", body_style))
    for item in [
        f"1. My name is <b>{claimant_name}</b> and I reside at <b>{claimant_address}</b>.",
        f"2. I am the <b>{claimant_type}</b> of the property located at <b>{property_address}</b>, {county} County, Georgia, Parcel ID: {parcel_id}.",
        f"3. The above property was sold at a tax sale on <b>{sale_date}</b>, generating surplus funds in the estimated amount of <b>${surplus_amount:,.2f}</b>.",
        f"4. I am entitled to claim these surplus funds as the {claimant_type} of record.",
        "5. I have not transferred, assigned, or conveyed my rights to these surplus funds to any other party.",
        "6. To the best of my knowledge, there are no other parties with a superior claim to these surplus funds.",
        "7. All statements made in this affidavit are true and correct to the best of my knowledge and belief."
    ]:
        story.append(Paragraph(item, body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("FURTHER AFFIANT SAYETH NOT.", normal_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("_______________________________", normal_style))
    story.append(Paragraph(f"{claimant_name}, Affiant", normal_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Sworn to and subscribed before me this _____ day of _____________, 20____</b>", normal_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("_______________________________", normal_style))
    story.append(Paragraph("Notary Public", normal_style))
    story.append(Paragraph("My Commission Expires: _______________", normal_style))
    story.append(PageBreak())

    # PAGE 3: MOTION FOR DISBURSEMENT
    story.append(Paragraph("MOTION FOR DISBURSEMENT OF SURPLUS FUNDS", title_style))
    story.append(Paragraph(f"In the Superior Court of {county} County, State of Georgia", center_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d')))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>Case/Parcel:</b> {parcel_id}", normal_style))
    story.append(Paragraph(f"<b>Property:</b> {property_address}", normal_style))
    story.append(Paragraph(f"<b>Sale Date:</b> {sale_date}", normal_style))
    story.append(Paragraph(f"<b>Surplus Amount:</b> ${surplus_amount:,.2f}", normal_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"NOW COMES {claimant_name.upper()}, Movant, and respectfully moves this Court to order the disbursement of surplus funds held by {county} County, Georgia, and in support thereof states:", body_style))
    for item in [
        f"1. On or about <b>{sale_date}</b>, the property located at <b>{property_address}</b>, {county} County, Georgia was sold at a tax sale.",
        f"2. The sale generated surplus funds in the amount of approximately <b>${surplus_amount:,.2f}</b> after satisfaction of all outstanding tax obligations.",
        f"3. Movant, <b>{claimant_name}</b>, is the {claimant_type} of the above-referenced property and is entitled to receive the surplus funds.",
        "4. Movant has provided all required documentation to support this claim, including an Affidavit of Claim and proof of identity.",
        "5. No other party has filed a claim to these surplus funds during the applicable claims period, or Movant's claim is superior to all other claims.",
    ]:
        story.append(Paragraph(item, body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"WHEREFORE, Movant respectfully requests that this Court enter an Order directing {county} County to disburse the surplus funds in the amount of ${surplus_amount:,.2f} to {claimant_name} at {claimant_address}.", body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Respectfully submitted,", normal_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("_______________________________", normal_style))
    story.append(Paragraph(claimant_name, normal_style))
    story.append(Paragraph(claimant_address, normal_style))
    story.append(Paragraph(claimant_email, normal_style))
    story.append(Paragraph(f"Date: {today}", normal_style))
    story.append(PageBreak())

    # PAGE 4: FILING INSTRUCTIONS
    story.append(Paragraph("FILING INSTRUCTIONS", title_style))
    story.append(Paragraph(f"{county} County, Georgia", center_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d')))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Follow these steps to file your surplus funds claim:", heading_style))
    for title, content in [
        ("<b>Step 1 — Notarize Your Affidavit</b>", "Take the Affidavit of Claim (Page 2) to a notary public. Sign in front of the notary and have them complete the notarization section. Banks, UPS Stores, and many courthouses offer notary services."),
        ("<b>Step 2 — Gather Supporting Documents</b>", "Collect: Government-issued photo ID, Proof of ownership or relationship to property (deed, probate documents), Social Security Number or Tax ID for disbursement."),
        ("<b>Step 3 — Submit Your Claim Package</b>", f"Deliver this complete package to the {county} County Tax Commissioner's office in person or by certified mail. Keep copies of everything."),
        ("<b>Step 4 — Follow Up</b>", "Follow up with the Tax Commissioner's office within 2-3 weeks to confirm receipt. Processing typically takes 30-90 days."),
        ("<b>Step 5 — Receive Payment</b>", "Upon approval, the county will issue a check or direct deposit for the surplus funds amount."),
    ]:
        story.append(Paragraph(title, subheading_style))
        story.append(Paragraph(content, body_style))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Important Notes:</b>", subheading_style))
    for note in [
        "- Claim deadlines vary by county. File as soon as possible.",
        "- If you have an attorney, have them review this package before filing.",
        "- Keep certified copies of all documents you submit.",
        "- Always verify county-specific requirements with the Tax Commissioner's office.",
    ]:
        story.append(Paragraph(note, normal_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Package generated by SurplusRecoveryPro on {today}", center_style))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    case_data = {
        "county": "Fulton",
        "property_address": "123 Peachtree St NW, Atlanta, GA 30303",
        "owner_name": "John Smith",
        "surplus_amount": 15420.50,
        "parcel_id": "14-0075-0002-019-3",
        "sale_date": "January 15, 2024",
        "case_number": "FC-2024-001234"
    }
    claimant_data = {
        "claimant_name": "John Smith",
        "claimant_address": "456 Oak Avenue, Atlanta, GA 30301",
        "claimant_email": "john.smith@email.com",
        "claimant_phone": "(404) 555-0123",
        "claimant_type": "owner"
    }
    output = generate_claim_package(case_data, claimant_data)
    print(f"Claim package generated: {output}")
