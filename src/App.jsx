export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" })
  }

  const { priceId, mode, userId, userEmail } = req.body

  if (!priceId || !mode) {
    return res.status(400).json({ error: "Missing priceId or mode" })
  }

  const origin = req.headers.origin || "https://surplus-recovery-pro-8he8.vercel.app"

  const params = new URLSearchParams({
    "payment_method_types[0]": "card",
    "mode": mode,
    "line_items[0][price]": priceId,
    "line_items[0][quantity]": "1",
    "success_url": `${origin}/?success=true`,
    "cancel_url": `${origin}/`,
  })

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
      return res.status(400).json({ error: session.error.message })
    }

    res.status(200).json({ url: session.url })
  } catch (error) {
    console.error("Stripe error:", error)
    res.status(500).json({ error: error.message })
  }
}
