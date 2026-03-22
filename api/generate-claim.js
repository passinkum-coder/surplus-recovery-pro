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

    // Insert claim package record via REST
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

    // Update with placeholder pdf_url
    await fetch(`${SUPABASE_URL}/rest/v1/claim_packages?id=eq.${claimPackage.id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`
      },
      body: JSON.stringify({
        status: 'complete',
        pdf_url: `https://surplusrecoverypro.site/api/claim-pdf/${claimPackage.id}`
      })
    })

    return res.status(200).json({
      success: true,
      package_id: claimPackage.id,
      message: 'Claim package is being generated'
    })

  } catch (err) {
    console.error('Claim generation error:', err)
    return res.status(500).json({ error: 'Failed to generate claim package: ' + err.message })
  }
}
