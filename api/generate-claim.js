export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const {
      county,
      property_address,
      surplus_amount,
      owner_name,
      claimant_name,
      claimant_address,
      claimant_email,
      claimant_phone,
      claimant_type,
      user_id
    } = req.body

    if (!user_id || !claimant_name || !claimant_address || !claimant_email) {
      return res.status(400).json({ error: 'Missing required fields' })
    }

    const SUPABASE_URL = process.env.SUPABASE_URL
    const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY
    const PDFSHIFT_API_KEY = process.env.PDFSHIFT_API_KEY

    const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
    const formattedAmount = surplus_amount ? '$' + Number(surplus_amount).toLocaleString() : 'To Be Determined'

    // 1. Insert claim package record
    const insertRes = await fetch(`${SUPABASE_URL}/rest/v1/claim_packages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
        'Prefer': 'return=representation'
      },
      body: JSON.stringify({
        user_id,
        county: county || '',
        property_address: property_address || '',
        claimant_name,
        claimant_type: claimant_type || 'Owner',
        surplus_amount: surplus_amount ? parseFloat(surplus_amount) : null,
        status: 'generating'
      })
    })

    const insertData = await insertRes.json()
    if (!insertRes.ok) throw new Error(JSON.stringify(insertData))
    const claimPackage = Array.isArray(insertData) ? insertData[0] : insertData

    // 2. Build HTML claim package from templates
    const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: Georgia, serif; color: #1a1a1a; margin: 0; padding: 0; font-size: 12pt; line-height: 1.6; }
  .page { padding: 1in; min-height: 9in; page-break-after: always; }
  .page:last-child { page-break-after: avoid; }
  h1 { font-size: 16pt; text-align: center; text-transform: uppercase; letter-spacing: 0.1em; border-bottom: 2px solid #1a1a1a; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
  h2 { font-size: 13pt; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1.5rem; }
  .label { font-size: 10pt; text-transform: uppercase; letter-spacing: 0.08em; color: #555; margin-bottom: 0.2rem; }
  .value { font-size: 12pt; border-bottom: 1px solid #999; padding-bottom: 0.2rem; margin-bottom: 1rem; min-height: 1.2rem; }
  .signature-line { border-bottom: 1px solid #1a1a1a; margin-top: 2rem; margin-bottom: 0.25rem; width: 60%; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  .header-info { text-align: right; margin-bottom: 2rem; }
  .county-address { margin-bottom: 2rem; }
  .re-line { margin: 1.5rem 0; font-weight: bold; }
  ol li { margin-bottom: 0.75rem; }
  .notary-box { border: 1px solid #1a1a1a; padding: 1rem; margin-top: 2rem; }
</style>
</head>
<body>

<!-- PAGE 1: COVER LETTER -->
<div class="page">
  <div class="header-info">
    <div>${claimant_name}</div>
    <div>${claimant_address}</div>
    <div>${claimant_email}</div>
    <div>${claimant_phone || ''}</div>
    <div style="margin-top:0.5rem">${today}</div>
  </div>

  <div class="county-address">
    <div>${county} County Clerk / Treasurer</div>
    <div>${county} County Courthouse</div>
    <div>${county}, Georgia</div>
  </div>

  <div class="re-line">RE: Claim for Surplus Funds — ${property_address || 'Property on File'} — Original Owner: ${owner_name || 'On File'}</div>

  <p>Dear ${county} County Clerk/Treasurer,</p>

  <p>I am writing to formally request the release of surplus funds in the amount of <strong>${formattedAmount}</strong> resulting from the tax sale or foreclosure of the above-referenced property. I am the ${claimant_type} and am entitled to claim these funds pursuant to applicable Georgia statutes.</p>

  <p>Enclosed with this letter you will find the following documents in support of this claim:</p>
  <ol>
    <li>Completed Surplus Funds Claim Form</li>
    <li>Proof of Ownership / Entitlement Affidavit</li>
    <li>Valid government-issued identification (to be attached)</li>
    <li>Supporting documentation establishing claimant's right to funds (to be attached)</li>
  </ol>

  <p>Please review the enclosed materials and process this claim at your earliest convenience. Should you require any additional information or documentation, please do not hesitate to contact me at ${claimant_email} or ${claimant_phone || 'the contact information above'}.</p>

  <p>Thank you for your time and attention to this matter.</p>

  <p style="margin-top: 2rem">Respectfully submitted,</p>
  <div class="signature-line"></div>
  <div>${claimant_name}</div>
  <div style="font-size:10pt; color:#555">${claimant_type} / Claimant</div>
  <div style="font-size:10pt; color:#555">${today}</div>
</div>

<!-- PAGE 2: CLAIM FORM -->
<div class="page">
  <h1>Surplus Funds Claim Form</h1>

  <h2>Section 1 — Claimant Information</h2>
  <div class="label">Full Legal Name</div>
  <div class="value">${claimant_name}</div>
  <div class="label">Mailing Address</div>
  <div class="value">${claimant_address}</div>
  <div class="two-col">
    <div>
      <div class="label">Email Address</div>
      <div class="value">${claimant_email}</div>
    </div>
    <div>
      <div class="label">Phone Number</div>
      <div class="value">${claimant_phone || ''}</div>
    </div>
  </div>
  <div class="label">Relationship to Property Owner</div>
  <div class="value">${claimant_type}</div>

  <h2>Section 2 — Property Information</h2>
  <div class="label">Original Property Owner</div>
  <div class="value">${owner_name || ''}</div>
  <div class="label">Property Address</div>
  <div class="value">${property_address || ''}</div>
  <div class="two-col">
    <div>
      <div class="label">County</div>
      <div class="value">${county}</div>
    </div>
    <div>
      <div class="label">Surplus Amount Claimed</div>
      <div class="value">${formattedAmount}</div>
    </div>
  </div>

  <h2>Section 3 — Certification</h2>
  <p>I, the undersigned, hereby certify under penalty of perjury that all information provided in this claim form is true, accurate, and complete to the best of my knowledge. I am legally entitled to claim the surplus funds described herein.</p>

  <div class="two-col" style="margin-top:2rem">
    <div>
      <div class="signature-line"></div>
      <div style="font-size:10pt">Claimant Signature</div>
    </div>
    <div>
      <div class="signature-line"></div>
      <div style="font-size:10pt">Date</div>
    </div>
  </div>
</div>

<!-- PAGE 3: AFFIDAVIT -->
<div class="page">
  <h1>Proof of Ownership / Entitlement Affidavit</h1>

  <p>STATE OF GEORGIA<br>COUNTY OF ${county}</p>

  <p>PERSONALLY APPEARED before me, the undersigned notary public, <strong>${claimant_name}</strong>, who, being duly sworn, deposes and states as follows:</p>

  <ol>
    <li>My name is <strong>${claimant_name}</strong> and I reside at <strong>${claimant_address}</strong>.</li>
    <li>I am the <strong>${claimant_type}</strong> of the property formerly owned by <strong>${owner_name || '________________'}</strong>, located at <strong>${property_address || '________________'}</strong>, in ${county} County, Georgia.</li>
    <li>Surplus funds in the amount of <strong>${formattedAmount}</strong> were generated as a result of a tax sale or foreclosure proceeding related to the above-referenced property.</li>
    <li>I am legally entitled to claim and receive these surplus funds pursuant to applicable Georgia law.</li>
    <li>No other person or entity has a superior claim to these surplus funds to the best of my knowledge.</li>
    <li>All information provided in support of this claim is true, accurate, and complete.</li>
  </ol>

  <p>FURTHER AFFIANT SAYETH NOT.</p>

  <div style="margin-top: 2rem">
    <div class="signature-line"></div>
    <div>${claimant_name} — Affiant</div>
  </div>

  <div class="notary-box">
    <p><strong>NOTARY PUBLIC</strong></p>
    <p>Sworn to and subscribed before me this ______ day of ________________, 20____.</p>
    <div class="signature-line"></div>
    <div style="font-size:10pt">Notary Public Signature</div>
    <div style="margin-top: 1rem; font-size:10pt">My Commission Expires: ______________________</div>
    <div style="margin-top: 0.5rem; font-size:10pt">[NOTARY SEAL]</div>
  </div>
</div>

<!-- PAGE 4: FILING INSTRUCTIONS -->
<div class="page">
  <h1>Filing Instructions</h1>
  <h2>${county} County Surplus Funds Claim — Step by Step Guide</h2>

  <p>Follow these steps carefully to file your surplus funds claim with ${county} County:</p>

  <ol>
    <li><strong>Gather your documents.</strong> Make sure you have all enclosed documents completed and signed. You will also need a valid government-issued photo ID (driver's license or passport) and any documents proving your relationship to the property (deed, probate records, etc.).</li>

    <li><strong>Get the Affidavit notarized.</strong> Take the Proof of Ownership / Entitlement Affidavit to a notary public. Do NOT sign it until you are in front of the notary. Notary services are available at most banks, UPS stores, and county courthouses.</li>

    <li><strong>Make copies.</strong> Make copies of all documents before submitting. Keep the originals for your records and submit copies, unless the county specifically requires originals.</li>

    <li><strong>Submit your claim.</strong> Deliver your completed claim package to the ${county} County Clerk or Treasurer's office. You may submit in person, by certified mail, or as directed by the county. Request a receipt or confirmation of filing.</li>

    <li><strong>Follow up.</strong> Processing times vary by county, typically 30–90 days. Follow up with the county office if you have not received a response within 60 days.</li>

    <li><strong>Receive your funds.</strong> Once approved, funds are typically issued by check to the claimant's address on file. Make sure your mailing address is current and accurate.</li>
  </ol>

  <h2>Important Notes</h2>
  <ul>
    <li>Deadlines apply — surplus funds may be forfeited if not claimed within the statutory period. File promptly.</li>
    <li>If your claim is denied, you have the right to appeal. Contact a licensed attorney for assistance.</li>
    <li>This package was prepared by SurplusRecoveryPro. For support, contact us at support@surplusrecoverypro.site.</li>
  </ul>

  <p style="margin-top: 2rem; font-size: 10pt; color: #555; border-top: 1px solid #ccc; padding-top: 1rem;">
    Generated by SurplusRecoveryPro on ${today} for ${claimant_name}. This document is for informational purposes and does not constitute legal advice. Consult a licensed attorney for legal guidance specific to your situation.
  </p>
</div>

</body>
</html>`

    // 3. Convert HTML to PDF using PDFShift
    const pdfRes = await fetch('https://api.pdfshift.io/v3/convert/pdf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + Buffer.from(`api:${PDFSHIFT_API_KEY}`).toString('base64')
      },
      body: JSON.stringify({
        source: html,
        landscape: false,
        use_print: false,
        margin: { top: '0.25in', bottom: '0.25in', left: '0.25in', right: '0.25in' }
      })
    })

    if (!pdfRes.ok) {
      const pdfError = await pdfRes.text()
      throw new Error('PDFShift error: ' + pdfError)
    }

    const pdfBuffer = await pdfRes.arrayBuffer()

    // 4. Upload PDF to Supabase Storage
    const fileName = `claim-${claimPackage.id}-${Date.now()}.pdf`
    const uploadRes = await fetch(`${SUPABASE_URL}/storage/v1/object/claim-packages/${fileName}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/pdf',
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
        'x-upsert': 'true'
      },
      body: pdfBuffer
    })

    if (!uploadRes.ok) {
      const uploadError = await uploadRes.text()
      throw new Error('Storage upload error: ' + uploadError)
    }

    // 5. Build public URL and update record
    const pdfUrl = `${SUPABASE_URL}/storage/v1/object/public/claim-packages/${fileName}`

    await fetch(`${SUPABASE_URL}/rest/v1/claim_packages?id=eq.${claimPackage.id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`
      },
      body: JSON.stringify({ status: 'complete', pdf_url: pdfUrl })
    })

    return res.status(200).json({
      success: true,
      package_id: claimPackage.id,
      message: 'Claim package generated successfully'
    })

  } catch (err) {
    console.error('Claim generation error:', err)
    return res.status(500).json({ error: 'Failed to generate claim package: ' + err.message })
  }
}
