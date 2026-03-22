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
      case_id,
      county,
      property_address,
      surplus_amount,
      parcel_id,
      sale_date,
      owner_name,
      claimant_name,
      claimant_address,
      claimant_email,
      claimant_phone,
      claimant_type,
      user_id
    } = req.body

    // Check user subscription tier
    const { data: profile } = await supabase
      .from('users')
      .select('subscription_tier')
      .eq('id', user_id)
      .single()

    if (!profile || profile.subscription_tier === 'basic') {
      return res.status(403).json({ 
        error: 'Claim Package Generator requires Professional or Premium plan' 
      })
    }

    // Store claim package record
    const { data: claimPackage, error } = await supabase
      .from('claim_packages')
      .insert({
        case_id,
        user_id,
        county,
        property_address,
        claimant_name,
        claimant_type,
        surplus_amount,
        status: 'generating'
      })
      .select()
      .single()

    if (error) throw error

    // Return package ID — frontend polls for completion
    return res.status(200).json({ 
      success: true,
      package_id: claimPackage.id,
      message: 'Claim package is being generated'
    })

  } catch (err) {
    console.error('Claim generation error:', err)
    return res.status(500).json({ error: 'Failed to generate claim package' })
  }
}
