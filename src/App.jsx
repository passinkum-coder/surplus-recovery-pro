import Stripe from "stripe"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" })
  }

  const { priceId, mode, userId, userEmail } = req.body

  if (!priceId || !mode) {
    return res.status(400).json({ error: "Missing priceId or mode" })
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      mode: mode, // "subscription" or "payment"
      line_items: [{ price: priceId, quantity: 1 }],
      customer_email: userEmail || undefined,
      metadata: { userId: userId || "" },
      success_url: `${req.headers.origin}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.origin}/`,
    })

    res.status(200).json({ url: session.url })
  } catch (error) {
    console.error("Stripe error:", error)
    res.status(500).json({ error: error.message })
  }
}
