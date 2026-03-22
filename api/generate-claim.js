import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
)

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

    // Store claim package record (no case_id to avoid foreign key constraint)
    const { data: claimPackage, error } = await supabase
      .from('claim_packages')
      .insert({
        user_id,
        county: county || '',
        property_address: property_address || '',
        claimant_name,
        claimant_type: claimant_type || 'Owner',
        surplus_amount: surplus_amount ? parseFloat(surplus_amount) : null,
        status: 'generating'
      })
      .select()
      .single()

    if (error) throw error

    // Mark as complete with placeholder URL
    await supabase
      .from('claim_packages')
      .update({ 
        status: 'complete',
        pdf_url: `https://surplusrecoverypro.site/api/claim-pdf/${claimPackage.id}`
      })
      .eq('id', claimPackage.id)

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
