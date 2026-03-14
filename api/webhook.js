import { createClient } from "@supabase/supabase-js"

const supabase = createClient(
  process.env.VITE_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
)

const PRICE_NAMES = {
  "price_1TADhnFtxvvfUBrHopwVlazJ": "Extra County Access",
  "price_1TADoUFtxvvfUBrHJAn3wSq6": "Lawyer Consultation",
  "price_1TADqMFtxvvfUBrHdFljkKR1": "Skip Trace Search",
  "price_1TADrYFtxvvfUBrH3zRaWGTw": "Document Notarization",
  "price_1TADsXFtxvvfUBrHKpqAJzV9": "Heir Research Report",
  "price_1TADtfFtxvvfUBrHPpqJvDG6": "Done-For-You Filing",
  "price_1TADwvFtxvvfUBrHK6ZdTggb": "Lead List Export",
  "price_1TADy3FtxvvfUBrHUFmDvLEu": "Training Course",
  "price_1TADP9FtxvvfUBrHq076N4HP": "Basic Plan",
  "price_1TADYEFtxvvfUBrHaWBDQHi1": "Professional Plan",
  "price_1TADc5FtxvvfUBrHh3ovZ1gA": "Premium Plan",
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" })
  }

  let event
  try {
    event = req.body
  } catch (err) {
    return res.status(400).json({ error: "Invalid payload" })
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object
    const userId = session.metadata?.userId
    const lineItems = session.line_items?.data
    const priceId = lineItems?.[0]?.price?.id || null

    if (userId) {
      const { error } = await supabase.from("purchases").insert({
        user_id: userId,
        price_id: priceId,
        product_name: PRICE_NAMES[priceId] || "Unknown",
        amount: session.amount_total ? session.amount_total / 100 : null,
        mode: session.mode,
        stripe_session_id: session.id,
      })
      if (error) console.error("Supabase insert error:", error)
    }
  }

  res.status(200).json({ received: true })
}

