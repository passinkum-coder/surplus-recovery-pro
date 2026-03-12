export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" })
  }

  const { priceId, mode, userId, userEmail } = req.body

  if (!priceId || !mode) {
    return res.status(400).json({ error: "Missing priceId or mode" })
  }

  if (!process.env.STRIPE_SECRET_KEY) {
    return res.status(500).json({ error: "Stripe key not configured" })
  }

  const origin = req.headers.origin || "https://surplus-recovery-pro-8he8.vercel.app"

  const params = new URLSearchParams()
  params.append("payment_method_types[0]", "card")
  params.append("mode", mode)
  params.append("line_items[0][price]", priceId)
  params.append("line_items[0][quantity]", "1")
  params.append("success_url", `${origin}/?success=true`)
  params.append("cancel_url", `${origin}/`)
  if (userEmail) params.append("customer_email", userEmail)
  if (userId) params.append("metadata[userId]", userId)

  try {
    const response = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.STRIPE_SECRET_KEY}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: params.toString(),
    })

    const session = await response.json()

    if (session.error) {
      console.error("Stripe error:", session.error)
      return res.status(400).json({ error: session.error.message })
    }

    res.status(200).json({ url: session.url })
  } catch (error) {
    console.error("Server error:", error)
    res.status(500).json({ error: error.message })
  }
}
