import { useState, useEffect, useRef } from "react"
import { createClient } from "@supabase/supabase-js"

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
)

const C = {
  bg: "#0a1628", card: "#0f2040", border: "#1a3058", gold: "#c9a84c",
  text: "#e8e0d0", muted: "#6b7a8d", light: "#a0aec0",
  green: "#22c55e", red: "#ef4444", purple: "#818cf8", nav: "#071020",
}

const tiers = [
  { name: "Basic", price: "$49", priceId: "price_1TADP9FtxvvfUBrHq076N4HP", featured: false, features: ["Single county access", "Owner contract templates", "Basic surplus search tools", "Claim status tracking", "Email support"] },
  { name: "Professional", price: "$149", priceId: "price_1TADYEFtxvvfUBrHaWBDQHi1", featured: true, features: ["Multi-county access (up to 5)", "Owner contract templates", "Document filing guides", "Claim status tracking", "Skip tracing (10/mo)", "Priority email support", "County auction alerts"] },
  { name: "Premium", price: "$349", priceId: "price_1TADc5FtxvvfUBrHh3ovZ1gA", featured: false, features: ["Unlimited county access", "Lawyer consultations (2/mo)", "Skip tracing (unlimited)", "Automated owner outreach", "Court filing assistance", "Heir research tools", "Lead list exports", "Dedicated account manager"] },
]

const addons = [
  { name: "Extra County Access", price: "$19/mo", priceId: "price_1TADhnFtxvvfUBrHopwVlazJ", mode: "subscription" },
  { name: "Lawyer Consultation", price: "$99/session", priceId: "price_1TADoUFtxvvfUBrHJAn3wSq6", mode: "payment" },
  { name: "Skip Trace Search", price: "$12/search", priceId: "price_1TADqMFtxvvfUBrHdFljkKR1", mode: "payment" },
  { name: "Document Notarization", price: "$29/doc", priceId: "price_1TADrYFtxvvfUBrH3zRaWGTw", mode: "payment" },
  { name: "Heir Research Report", price: "$79/report", priceId: "price_1TADsXFtxvvfUBrHKpqAJzV9", mode: "payment" },
  { name: "Done-For-You Filing", price: "$199/claim", priceId: "price_1TADtfFtxvvfUBrHPpqJvDG6", mode: "payment" },
  { name: "Lead List Export", price: "$49/export", priceId: "price_1TADwvFtxvvfUBrHK6ZdTggb", mode: "payment" },
  { name: "Training Course", price: "$299 one-time", priceId: "price_1TADy3FtxvvfUBrHUFmDvLEu", mode: "payment" },
]

const US_STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

function Badge({ status }) {
  const map = {
    Active: { bg: "rgba(201,168,76,0.15)", c: "#c9a84c" },
    Pending: { bg: "rgba(240,180,41,0.15)", c: "#f0b429" },
    Filed: { bg: "rgba(129,140,248,0.15)", c: "#818cf8" },
    Complete: { bg: "rgba(34,197,94,0.15)", c: "#22c55e" },
  }
  const s = map[status] || map.Pending
  return (
    <span style={{ background: s.bg, color: s.c, padding: "0.2rem 0.6rem", borderRadius: "3px", fontSize: "0.72rem", fontWeight: "bold", letterSpacing: "0.05em", textTransform: "uppercase" }}>
      {status}
    </span>
  )
}

function Avatar({ name, size = 36 }) {
  const initials = name ? name.split(" ").map(function(w) { return w[0] }).join("").toUpperCase().slice(0, 2) : "?"
  return (
    <div style={{ width: size, height: size, borderRadius: "50%", background: C.gold, color: "#0a1628", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold", fontSize: size * 0.38 + "px", fontFamily: "Georgia, serif", cursor: "pointer", flexShrink: 0 }}>
      {initials}
    </div>
  )
}

function PricingCard({ t, hoveredTier, setHoveredTier, onGetStarted, onCheckout }) {
  const isHovered = hoveredTier === t.name
  const isActive = hoveredTier === null ? t.featured : isHovered
  return (
    <div
      onMouseEnter={() => setHoveredTier(t.name)}
      onMouseLeave={() => setHoveredTier(null)}
      style={{ background: isHovered ? "#162a52" : C.card, borderTop: "3px solid " + (isActive ? C.gold : C.border), border: "1px solid " + (isActive ? C.gold : C.border), borderRadius: "4px", padding: "1.75rem", position: "relative", transition: "all 0.2s", cursor: "pointer" }}
    >
      {t.featured && (
        <div style={{ position: "absolute", top: "-11px", left: "50%", transform: "translateX(-50%)", background: C.gold, color: "#0a1628", padding: "0.18rem 0.9rem", fontSize: "0.68rem", fontWeight: "bold", letterSpacing: "0.1em", textTransform: "uppercase", whiteSpace: "nowrap" }}>
          MOST POPULAR
        </div>
      )}
      <div style={{ fontSize: "0.75rem", fontWeight: "bold", color: C.muted, textTransform: "uppercase", letterSpacing: "0.15em", marginBottom: "0.6rem" }}>{t.name}</div>
      <div style={{ fontSize: "2.8rem", fontWeight: "bold", color: "#fff", fontFamily: "Georgia, serif", marginBottom: "0.2rem" }}>{t.price}</div>
      <div style={{ fontSize: "0.75rem", color: C.muted, marginBottom: "1.5rem", letterSpacing: "0.05em" }}>PER MONTH</div>
      <ul style={{ listStyle: "none", padding: 0, margin: "0 0 1.75rem" }}>
        {t.features.map(function(f) {
          return (
            <li key={f} style={{ display: "flex", gap: "0.6rem", padding: "0.42rem 0", fontSize: "0.85rem", color: C.light, borderBottom: "1px solid " + C.border }}>
              <span style={{ color: C.gold, flexShrink: 0 }}>✓</span>{f}
            </li>
          )
        })}
      </ul>
      <button onClick={onCheckout} style={{ width: "100%", padding: "0.8rem", borderRadius: "3px", border: isActive ? "none" : "1px solid " + C.border, background: isActive ? C.gold : "transparent", color: isActive ? "#0a1628" : C.light, fontWeight: "bold", cursor: "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.07em", fontSize: "0.82rem", textTransform: "uppercase", transition: "all 0.2s" }}>
        Get Started
      </button>
    </div>
  )
}

export default function App() {
  const [page, setPage] = useState("home")
  const [modal, setModal] = useState(null)
  const [mode, setMode] = useState("login")
  const [user, setUser] = useState(null)
  const [form, setForm] = useState({ name: "", email: "", password: "" })
  const [authError, setAuthError] = useState("")
  const [loading, setLoading] = useState(false)
  const [hoveredTier, setHoveredTier] = useState(null)
  const [forgotSent, setForgotSent] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [claims, setClaims] = useState([])
  const [claimsLoading, setClaimsLoading] = useState(false)
  const [newClaim, setNewClaim] = useState({ owner_name: "", county: "", state: "", amount: "", notes: "" })
  const [claimError, setClaimError] = useState("")
  const [claimSaving, setClaimSaving] = useState(false)
  const [avatarOpen, setAvatarOpen] = useState(false)
  const [profileForm, setProfileForm] = useState({ full_name: "", newPassword: "", confirmPassword: "" })
  const [profileMsg, setProfileMsg] = useState("")
  const [profileSaving, setProfileSaving] = useState(false)
  const avatarRef = useRef(null)
  const chatEndRef = useRef(null)
  const [chatOpen, setChatOpen] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)

  useEffect(function() {
    const params = new URLSearchParams(window.location.search)
    if (params.get('success') === 'true') {
      window.history.replaceState({}, '', '/')
    }
  }, [])

  useEffect(function() {
    supabase.auth.getSession().then(function(result) {
      if (result.data.session) {
        setUser(result.data.session.user)
        setPage("dashboard")
      }
    })
    const listener = supabase.auth.onAuthStateChange(function(event, session) {
      if (session) {
        setUser(session.user)
        setPage("dashboard")
      } else {
        setUser(null)
        setPage("home")
        setClaims([])
      }
    })
    return function() { listener.data.subscription.unsubscribe() }
  }, [])

  useEffect(function() {
    if (page === "dashboard" && user) fetchClaims()
  }, [page, user])

  useEffect(function() {
    if (chatEndRef.current) chatEndRef.current.scrollIntoView({ behavior: "smooth" })
  }, [chatMessages])

  useEffect(function() {
    if (page === "profile" && user) {
      setProfileForm({ full_name: userName || "", newPassword: "", confirmPassword: "" })
      setProfileMsg("")
    }
  }, [page])

  useEffect(function() {
    function handleClick(e) {
      if (avatarRef.current && !avatarRef.current.contains(e.target)) {
        setAvatarOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClick)
    return function() { document.removeEventListener("mousedown", handleClick) }
  }, [])

  async function fetchClaims() {
    setClaimsLoading(true)
    const { data, error } = await supabase.from("claims").select("*").order("created_at", { ascending: false })
    if (!error && data) setClaims(data)
    setClaimsLoading(false)
  }

  async function handleSaveClaim(e) {
    e.preventDefault()
    setClaimError("")
    if (!newClaim.owner_name || !newClaim.county || !newClaim.state) {
      setClaimError("Owner name, county, and state are required.")
      return
    }
    setClaimSaving(true)
    const { error } = await supabase.from("claims").insert({
      user_id: user.id,
      owner_name: newClaim.owner_name,
      county: newClaim.county,
      state: newClaim.state,
      amount: newClaim.amount ? parseFloat(newClaim.amount.replace(/[^0-9.]/g, "")) : null,
      notes: newClaim.notes,
      status: "Pending",
    })
    setClaimSaving(false)
    if (error) {
      setClaimError(error.message)
    } else {
      setModal(null)
      setNewClaim({ owner_name: "", county: "", state: "", amount: "", notes: "" })
      fetchClaims()
    }
  }

  async function handleSaveProfile(e) {
    e.preventDefault()
    setProfileMsg("")
    setProfileSaving(true)
    if (profileForm.newPassword) {
      if (profileForm.newPassword !== profileForm.confirmPassword) {
        setProfileMsg("error:Passwords do not match.")
        setProfileSaving(false)
        return
      }
      if (profileForm.newPassword.length < 6) {
        setProfileMsg("error:Password must be at least 6 characters.")
        setProfileSaving(false)
        return
      }
    }
    const updates = {}
    if (profileForm.full_name) updates.data = { full_name: profileForm.full_name }
    if (profileForm.newPassword) updates.password = profileForm.newPassword
    const { error } = await supabase.auth.updateUser(updates)
    setProfileSaving(false)
    if (error) {
      setProfileMsg("error:" + error.message)
    } else {
      setProfileMsg("success:Profile updated successfully!")
      setProfileForm(function(p) { return { ...p, newPassword: "", confirmPassword: "" } })
      supabase.auth.getUser().then(function(result) { if (result.data.user) setUser(result.data.user) })
    }
  }

  async function handleLogin(e) {
    e.preventDefault()
    setAuthError("")
    setLoading(true)
    if (mode === "signup") {
      const { error } = await supabase.auth.signUp({
        email: form.email,
        password: form.password,
        options: { data: { full_name: form.name } }
      })
      if (error) { setAuthError(error.message) } else { setAuthError("Check your email to confirm your account!") }
    } else {
      const { error } = await supabase.auth.signInWithPassword({ email: form.email, password: form.password })
      if (error) { setAuthError(error.message) } else { setModal(null) }
    }
    setLoading(false)
  }

  async function handleForgot(e) {
    e.preventDefault()
    setLoading(true)
    setAuthError("")
    const { error } = await supabase.auth.resetPasswordForEmail(form.email, { redirectTo: window.location.origin })
    setLoading(false)
    if (error) { setAuthError(error.message) } else { setForgotSent(true) }
  }

  async function handleLogout() {
    await supabase.auth.signOut()
    setUser(null)
    setPage("home")
  }

  async function sendChat(e) {
    e.preventDefault()
    if (!chatInput.trim() || chatLoading) return
    const userMsg = { role: "user", content: chatInput }
    setChatMessages(function(prev) { return [...prev, userMsg] })
    setChatInput("")
    setChatLoading(true)
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: "You are a helpful assistant for SurplusRecoveryPro, a platform for surplus fund recovery professionals. Help users with questions about surplus funds, tax deeds, foreclosure overages, claim filing, skip tracing, and how to use the platform. Be concise and professional.",
          messages: [...chatMessages, userMsg].map(function(m) { return { role: m.role, content: m.content } })
        })
      })
      const data = await response.json()
      const reply = data.content && data.content[0] && data.content[0].text ? data.content[0].text : "Sorry, I could not get a response."
      setChatMessages(function(prev) { return [...prev, { role: "assistant", content: reply }] })
    } catch(err) {
      setChatMessages(function(prev) { return [...prev, { role: "assistant", content: "Sorry, something went wrong. Please try again." }] })
    }
    setChatLoading(false)
  }

  async function handleCheckout(priceId, mode) {
    if (!user) { openAuth("signup"); return }
    try {
      const response = await fetch("/api/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ priceId, mode, userId: user.id, userEmail: user.email })
      })
      const data = await response.json()
      if (data.url) { window.location.href = data.url }
      else { alert("Something went wrong. Please try again.") }
    } catch (err) {
      alert("Something went wrong. Please try again.")
    }
  }

  function openAuth(m) {
    setMode(m)
    setModal("auth")
    setAuthError("")
    setForgotSent(false)
  }

  const navStyle = {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    padding: "0 2rem", height: "58px", background: C.nav,
    borderBottom: "3px solid " + C.gold, position: "sticky", top: 0, zIndex: 100,
  }

  const inputStyle = {
    width: "100%", padding: "0.7rem", background: "#071020",
    border: "1px solid " + C.border, borderRadius: "3px", color: C.text,
    fontSize: "0.9rem", marginBottom: "1rem", boxSizing: "border-box",
    fontFamily: "Georgia, serif", outline: "none",
  }

  const labelStyle = {
    display: "block", fontSize: "0.68rem", color: C.muted, textTransform: "uppercase",
    letterSpacing: "0.12em", marginBottom: "0.35rem",
  }

  const userName = user && (user.user_metadata && user.user_metadata.full_name ? user.user_metadata.full_name : user.email.split("@")[0])

  const totalRecovered = claims.reduce(function(sum, c) { return sum + (c.amount || 0) }, 0)
  const pendingClaims = claims.filter(function(c) { return c.status === "Pending" }).length
  const counties = new Set(claims.map(function(c) { return c.county + "," + c.state })).size

  function formatAmount(n) { return n ? "$" + Number(n).toLocaleString() : "-" }
  function formatDate(d) { return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) }

  const DashNav = (
    <div style={navStyle}>
      <span style={{ color: C.gold, fontWeight: "bold", letterSpacing: "0.08em", cursor: "pointer", fontSize: "1.1rem" }} onClick={() => setPage("dashboard")}>SURPLUS RECOVERY PRO</span>
      <div style={{ display: "flex", gap: "1.25rem", alignItems: "center" }}>
        <span style={{ color: C.muted, fontSize: "0.8rem", letterSpacing: "0.05em", display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <span style={{ color: C.gold }}>PROFESSIONAL</span>
        </span>
        <div ref={avatarRef} style={{ position: "relative" }}>
          <div onClick={() => setAvatarOpen(!avatarOpen)}>
            <Avatar name={userName} size={36} />
          </div>
          {avatarOpen && (
            <div style={{ position: "absolute", right: 0, top: "46px", background: C.card, border: "1px solid " + C.border, borderRadius: "4px", minWidth: "180px", zIndex: 200, overflow: "hidden" }}>
              <div style={{ padding: "0.85rem 1rem", borderBottom: "1px solid " + C.border }}>
                <div style={{ fontSize: "0.88rem", fontWeight: "bold", color: "#fff" }}>{userName}</div>
                <div style={{ fontSize: "0.75rem", color: C.muted, marginTop: "0.15rem" }}>{user && user.email}</div>
              </div>
              <div
                onClick={() => { setPage("profile"); setAvatarOpen(false) }}
                style={{ padding: "0.75rem 1rem", cursor: "pointer", fontSize: "0.85rem", color: C.light, borderBottom: "1px solid " + C.border }}
                onMouseEnter={function(e) { e.target.style.background = "#162a52" }}
                onMouseLeave={function(e) { e.target.style.background = "transparent" }}
              >
                My Profile
              </div>
              <div
                onClick={() => { setPage("dashboard"); setAvatarOpen(false) }}
                style={{ padding: "0.75rem 1rem", cursor: "pointer", fontSize: "0.85rem", color: C.light, borderBottom: "1px solid " + C.border }}
                onMouseEnter={function(e) { e.target.style.background = "#162a52" }}
                onMouseLeave={function(e) { e.target.style.background = "transparent" }}
              >
                Dashboard
              </div>
              <div
                onClick={handleLogout}
                style={{ padding: "0.75rem 1rem", cursor: "pointer", fontSize: "0.85rem", color: C.red }}
                onMouseEnter={function(e) { e.target.style.background = "#162a52" }}
                onMouseLeave={function(e) { e.target.style.background = "transparent" }}
              >
                Sign Out
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )

  if (page === "profile" && user) {
    const isError = profileMsg.startsWith("error:")
    const msgText = profileMsg.replace(/^(error:|success:)/, "")
    return (
      <div style={{ minHeight: "100vh", background: C.bg, color: C.text, fontFamily: "Georgia, serif" }}>
        {DashNav}
        <div style={{ maxWidth: "640px", margin: "0 auto", padding: "2.5rem 2rem" }}>
          <div style={{ marginBottom: "2rem" }}>
            <div style={{ fontSize: "0.7rem", color: C.gold, textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "0.4rem" }}>Account</div>
            <div style={{ fontSize: "1.6rem", fontWeight: "bold", color: "#fff" }}>My Profile</div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "1.25rem", background: C.card, border: "1px solid " + C.border, borderRadius: "4px", padding: "1.5rem", marginBottom: "1.5rem" }}>
            <Avatar name={userName} size={56} />
            <div>
              <div style={{ fontSize: "1.1rem", fontWeight: "bold", color: "#fff" }}>{userName}</div>
              <div style={{ fontSize: "0.82rem", color: C.muted, marginTop: "0.2rem" }}>{user.email}</div>
              <div style={{ fontSize: "0.72rem", color: C.gold, marginTop: "0.3rem", textTransform: "uppercase", letterSpacing: "0.1em" }}>Professional Plan</div>
            </div>
          </div>

          <form onSubmit={handleSaveProfile}>
            <div style={{ background: C.card, border: "1px solid " + C.border, borderRadius: "4px", padding: "1.5rem", marginBottom: "1.5rem" }}>
              <div style={{ fontSize: "0.78rem", fontWeight: "bold", color: "#fff", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "1.25rem" }}>Account Details</div>
              <div style={{ marginBottom: "1rem" }}>
                <label style={labelStyle}>Full Name</label>
                <input style={inputStyle} value={profileForm.full_name} onChange={function(e) { setProfileForm({ ...profileForm, full_name: e.target.value }) }} placeholder="Your full name" />
              </div>
              <div>
                <label style={labelStyle}>Email Address</label>
                <input style={{ ...inputStyle, opacity: 0.5, cursor: "not-allowed" }} value={user.email} disabled />
                <div style={{ fontSize: "0.73rem", color: C.muted, marginTop: "-0.75rem", marginBottom: "1rem" }}>Email cannot be changed here</div>
              </div>
            </div>

            <div style={{ background: C.card, border: "1px solid " + C.border, borderRadius: "4px", padding: "1.5rem", marginBottom: "1.5rem" }}>
              <div style={{ fontSize: "0.78rem", fontWeight: "bold", color: "#fff", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "1.25rem" }}>Change Password</div>
              <div style={{ marginBottom: "1rem" }}>
                <label style={labelStyle}>New Password</label>
                <div style={{ position: "relative" }}>
                  <input style={{ ...inputStyle, marginBottom: 0, paddingRight: "2.5rem" }} type={showPassword ? "text" : "password"} value={profileForm.newPassword} onChange={function(e) { setProfileForm({ ...profileForm, newPassword: e.target.value }) }} placeholder="Leave blank to keep current" />
                  <span onClick={() => setShowPassword(!showPassword)} style={{ position: "absolute", right: "0.75rem", top: "50%", transform: "translateY(-50%)", cursor: "pointer", color: C.muted, fontSize: "0.75rem" }}>{showPassword ? "HIDE" : "SHOW"}</span>
                </div>
              </div>
              <div>
                <label style={labelStyle}>Confirm New Password</label>
                <input style={inputStyle} type="password" value={profileForm.confirmPassword} onChange={function(e) { setProfileForm({ ...profileForm, confirmPassword: e.target.value }) }} placeholder="Repeat new password" />
              </div>
            </div>

            <div style={{ background: C.card, border: "1px solid " + C.border, borderRadius: "4px", padding: "1.5rem", marginBottom: "1.5rem" }}>
              <div style={{ fontSize: "0.78rem", fontWeight: "bold", color: "#fff", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "1rem" }}>Current Plan</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
                <div>
                  <div style={{ fontSize: "1.2rem", fontWeight: "bold", color: C.gold }}>Professional</div>
                  <div style={{ fontSize: "0.82rem", color: C.muted, marginTop: "0.2rem" }}>$149/month - Multi-county access, skip tracing, priority support</div>
                </div>
                <button type="button" onClick={() => { setPage("home"); setTimeout(function() { document.getElementById("pricing") && document.getElementById("pricing").scrollIntoView({ behavior: "smooth" }) }, 100) }} style={{ padding: "0.55rem 1.2rem", border: "1px solid " + C.gold, borderRadius: "3px", background: "transparent", color: C.gold, cursor: "pointer", fontFamily: "Georgia, serif", fontSize: "0.8rem", letterSpacing: "0.06em", fontWeight: "bold" }}>UPGRADE PLAN</button>
              </div>
            </div>

            <div style={{ background: C.card, border: "1px solid " + C.border, borderRadius: "4px", padding: "1.5rem", marginBottom: "1.5rem" }}>
              <div style={{ fontSize: "0.78rem", fontWeight: "bold", color: "#fff", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "1rem" }}>Billing History</div>
              <div style={{ color: C.muted, fontSize: "0.85rem" }}>No billing history yet. Billing history will appear here once Stripe payments are connected.</div>
            </div>

            {profileMsg && (
              <div style={{ background: isError ? "rgba(239,68,68,0.1)" : "rgba(34,197,94,0.1)", border: "1px solid " + (isError ? C.red : C.green), borderRadius: "3px", padding: "0.75rem", marginBottom: "1rem", fontSize: "0.83rem", color: isError ? C.red : C.green }}>
                {msgText}
              </div>
            )}

            <div style={{ display: "flex", gap: "1rem" }}>
              <button type="button" onClick={() => setPage("dashboard")} style={{ flex: 1, padding: "0.85rem", background: "transparent", color: C.light, border: "1px solid " + C.border, borderRadius: "3px", fontWeight: "bold", cursor: "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", textTransform: "uppercase", fontSize: "0.9rem" }}>Cancel</button>
              <button type="submit" disabled={profileSaving} style={{ flex: 2, padding: "0.85rem", background: profileSaving ? C.muted : C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: profileSaving ? "not-allowed" : "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", textTransform: "uppercase", fontSize: "0.9rem" }}>{profileSaving ? "Saving..." : "Save Changes"}</button>
            </div>
          </form>
        </div>
      </div>
    )
  }

  if (page === "dashboard" && user) {
    return (
      <div style={{ minHeight: "100vh", background: C.bg, color: C.text, fontFamily: "Georgia, serif" }}>
        {DashNav}
        <div style={{ padding: "2rem 2.5rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "2rem", flexWrap: "wrap", gap: "1rem" }}>
            <div>
              <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#fff", marginBottom: "0.25rem" }}>Welcome back, {userName}</div>
              <div style={{ color: C.muted, fontSize: "0.8rem", letterSpacing: "0.08em", textTransform: "uppercase" }}>Surplus Recovery Dashboard - Professional Plan</div>
            </div>
            <button onClick={() => { setClaimError(""); setModal("newclaim") }} style={{ padding: "0.65rem 1.4rem", background: C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.06em", fontSize: "0.85rem" }}>+ NEW CLAIM</button>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))", gap: "1.25rem", marginBottom: "2rem" }}>
            {[
              { l: "Total Claims", v: String(claims.length), s: "in your account", c: C.gold },
              { l: "Total Recovered", v: "$" + totalRecovered.toLocaleString(), s: "across all claims", c: C.green },
              { l: "Counties Tracked", v: String(counties), s: "unique counties", c: C.purple },
              { l: "Pending Claims", v: String(pendingClaims), s: "awaiting action", c: C.red },
            ].map(function(x) {
              return (
                <div key={x.l} style={{ background: C.card, borderTop: "3px solid " + x.c, border: "1px solid " + C.border, borderRadius: "4px", padding: "1.4rem" }}>
                  <div style={{ fontSize: "0.68rem", color: C.muted, textTransform: "uppercase", letterSpacing: "0.13em", marginBottom: "0.6rem" }}>{x.l}</div>
                  <div style={{ fontSize: "1.9rem", fontWeight: "bold", color: "#fff", marginBottom: "0.2rem" }}>{x.v}</div>
                  <div style={{ fontSize: "0.78rem", color: x.c }}>{x.s}</div>
                </div>
              )
            })}
          </div>

          <div style={{ background: C.card, border: "1px solid " + C.border, borderRadius: "4px", overflow: "hidden" }}>
            <div style={{ padding: "1rem 1.5rem", borderBottom: "1px solid " + C.border, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontWeight: "bold", color: "#fff", fontSize: "0.85rem", textTransform: "uppercase", letterSpacing: "0.08em" }}>Your Claims</span>
              <span style={{ fontSize: "0.78rem", color: C.gold, letterSpacing: "0.05em" }}>{claims.length} TOTAL</span>
            </div>
            {claimsLoading ? (
              <div style={{ padding: "2rem", textAlign: "center", color: C.muted }}>Loading claims...</div>
            ) : claims.length === 0 ? (
              <div style={{ padding: "3rem", textAlign: "center" }}>
                <div style={{ color: C.muted, marginBottom: "1rem", fontSize: "0.9rem" }}>No claims yet. Add your first claim to get started.</div>
                <button onClick={() => { setClaimError(""); setModal("newclaim") }} style={{ padding: "0.65rem 1.4rem", background: C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: "pointer", fontFamily: "Georgia, serif", fontSize: "0.82rem" }}>+ ADD FIRST CLAIM</button>
              </div>
            ) : (
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ background: "#071020" }}>
                    {["Owner", "County", "State", "Amount", "Status", "Date Added"].map(function(h) {
                      return <th key={h} style={{ padding: "0.7rem 1.25rem", textAlign: "left", fontSize: "0.68rem", color: C.muted, textTransform: "uppercase", letterSpacing: "0.12em", borderBottom: "1px solid " + C.border }}>{h}</th>
                    })}
                  </tr>
                </thead>
                <tbody>
                  {claims.map(function(r, i) {
                    return (
                      <tr key={r.id} style={{ background: i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.015)" }}>
                        <td style={{ padding: "0.9rem 1.25rem", color: C.gold, fontSize: "0.88rem", fontWeight: "bold" }}>{r.owner_name}</td>
                        <td style={{ padding: "0.9rem 1.25rem", color: C.text, fontSize: "0.88rem" }}>{r.county}</td>
                        <td style={{ padding: "0.9rem 1.25rem", color: C.light, fontSize: "0.82rem" }}>{r.state}</td>
                        <td style={{ padding: "0.9rem 1.25rem", color: "#fff", fontWeight: "bold", fontSize: "0.88rem" }}>{formatAmount(r.amount)}</td>
                        <td style={{ padding: "0.9rem 1.25rem" }}><Badge status={r.status} /></td>
                        <td style={{ padding: "0.9rem 1.25rem", color: C.muted, fontSize: "0.82rem" }}>{formatDate(r.created_at)}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {modal === "newclaim" && (
          <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 200, padding: "1rem" }} onClick={() => setModal(null)}>
            <div style={{ background: C.card, border: "1px solid " + C.border, borderTop: "3px solid " + C.gold, borderRadius: "4px", padding: "2.25rem", width: "100%", maxWidth: "460px", position: "relative", maxHeight: "90vh", overflowY: "auto" }} onClick={function(e) { e.stopPropagation() }}>
              <button onClick={() => setModal(null)} style={{ position: "absolute", top: "0.75rem", right: "1rem", background: "none", border: "none", color: C.muted, fontSize: "1.4rem", cursor: "pointer" }}>x</button>
              <div style={{ fontSize: "0.68rem", color: C.gold, textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "0.4rem" }}>New Claim</div>
              <div style={{ fontSize: "1.4rem", fontWeight: "bold", color: "#fff", marginBottom: "0.25rem", fontFamily: "Georgia, serif" }}>Add a Surplus Claim</div>
              <div style={{ color: C.muted, fontSize: "0.83rem", marginBottom: "1.75rem" }}>Enter the property owner and surplus details</div>
              {claimError && <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid " + C.red, borderRadius: "3px", padding: "0.75rem", marginBottom: "1rem", fontSize: "0.83rem", color: C.red }}>{claimError}</div>}
              <form onSubmit={handleSaveClaim}>
                <div style={{ marginBottom: "1rem" }}>
                  <label style={labelStyle}>Owner Name *</label>
                  <input style={inputStyle} placeholder="e.g. James Wilson" value={newClaim.owner_name} onChange={function(e) { setNewClaim({ ...newClaim, owner_name: e.target.value }) }} />
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "1rem" }}>
                  <div>
                    <label style={labelStyle}>County *</label>
                    <input style={{ ...inputStyle, marginBottom: 0 }} placeholder="e.g. Cook County" value={newClaim.county} onChange={function(e) { setNewClaim({ ...newClaim, county: e.target.value }) }} />
                  </div>
                  <div>
                    <label style={labelStyle}>State *</label>
                    <select style={{ ...inputStyle, marginBottom: 0 }} value={newClaim.state} onChange={function(e) { setNewClaim({ ...newClaim, state: e.target.value }) }}>
                      <option value="">Select state</option>
                      {US_STATES.map(function(s) { return <option key={s} value={s}>{s}</option> })}
                    </select>
                  </div>
                </div>
                <div style={{ marginBottom: "1rem" }}>
                  <label style={labelStyle}>Surplus Amount</label>
                  <input style={inputStyle} placeholder="e.g. 12400" value={newClaim.amount} onChange={function(e) { setNewClaim({ ...newClaim, amount: e.target.value }) }} />
                </div>
                <div style={{ marginBottom: "1.5rem" }}>
                  <label style={labelStyle}>Notes</label>
                  <textarea style={{ ...inputStyle, marginBottom: 0, minHeight: "80px", resize: "vertical" }} placeholder="Any additional details..." value={newClaim.notes} onChange={function(e) { setNewClaim({ ...newClaim, notes: e.target.value }) }} />
                </div>
                <button type="submit" disabled={claimSaving} style={{ width: "100%", padding: "0.85rem", background: claimSaving ? C.muted : C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: claimSaving ? "not-allowed" : "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", textTransform: "uppercase", fontSize: "0.9rem" }}>
                  {claimSaving ? "Saving..." : "Save Claim"}
                </button>
              </form>
            </div>
          </div>
        )}

        {chatOpen && (
          <div style={{ position: "fixed", bottom: "80px", right: "1.5rem", width: "340px", height: "460px", background: C.card, border: "1px solid " + C.border, borderTop: "3px solid " + C.gold, borderRadius: "4px", zIndex: 300, display: "flex", flexDirection: "column", boxShadow: "0 8px 32px rgba(0,0,0,0.4)" }}>
            <div style={{ padding: "0.9rem 1.25rem", borderBottom: "1px solid " + C.border, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontWeight: "bold", color: "#fff", fontSize: "0.88rem", letterSpacing: "0.05em" }}>SRP Assistant</div>
                <div style={{ fontSize: "0.7rem", color: C.gold, letterSpacing: "0.08em" }}>AI-POWERED SUPPORT</div>
              </div>
              <button onClick={() => setChatOpen(false)} style={{ background: "none", border: "none", color: C.muted, fontSize: "1.2rem", cursor: "pointer" }}>x</button>
            </div>
            <div style={{ flex: 1, overflowY: "auto", padding: "1rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {chatMessages.length === 0 && (
                <div style={{ textAlign: "center", color: C.muted, fontSize: "0.82rem", marginTop: "2rem", lineHeight: 1.6 }}>
                  Hi {userName}! Ask me anything about surplus recovery, claims, or how to use the platform.
                </div>
              )}
              {chatMessages.map(function(m, i) {
                return (
                  <div key={i} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
                    <div style={{ maxWidth: "80%", padding: "0.6rem 0.9rem", borderRadius: "4px", fontSize: "0.83rem", lineHeight: 1.5, background: m.role === "user" ? C.gold : "#162a52", color: m.role === "user" ? "#0a1628" : C.text, fontWeight: m.role === "user" ? "bold" : "normal" }}>
                      {m.content}
                    </div>
                  </div>
                )
              })}
              {chatLoading && (
                <div style={{ display: "flex", justifyContent: "flex-start" }}>
                  <div style={{ background: "#162a52", padding: "0.6rem 0.9rem", borderRadius: "4px", fontSize: "0.83rem", color: C.muted }}>...</div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
            <form onSubmit={sendChat} style={{ padding: "0.75rem", borderTop: "1px solid " + C.border, display: "flex", gap: "0.5rem" }}>
              <input
                value={chatInput}
                onChange={function(e) { setChatInput(e.target.value) }}
                placeholder="Ask a question..."
                style={{ flex: 1, padding: "0.6rem 0.75rem", background: "#071020", border: "1px solid " + C.border, borderRadius: "3px", color: C.text, fontSize: "0.83rem", fontFamily: "Georgia, serif", outline: "none" }}
              />
              <button type="submit" disabled={chatLoading} style={{ padding: "0.6rem 0.9rem", background: C.gold, border: "none", borderRadius: "3px", color: "#0a1628", fontWeight: "bold", cursor: chatLoading ? "not-allowed" : "pointer", fontSize: "0.82rem", fontFamily: "Georgia, serif" }}>
                Send
              </button>
            </form>
          </div>
        )}

        <button
          onClick={() => setChatOpen(!chatOpen)}
          style={{ position: "fixed", bottom: "1.5rem", right: "1.5rem", width: "36px", height: "36px", borderRadius: "50% 50% 50% 0", background: C.gold, border: "none", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 4px 16px rgba(201,168,76,0.4)", zIndex: 300, transform: "rotate(-45deg)" }}
        >
          <div style={{ transform: "rotate(45deg)", display: "flex", gap: "3px", alignItems: "center" }}>
            {chatOpen ? <span style={{ fontSize: "1rem", color: "#0a1628", fontWeight: "bold", lineHeight: 1 }}>✕</span> : [<span key="1" style={{ width: "5px", height: "5px", borderRadius: "50%", background: "#0a1628", display: "inline-block" }}></span>, <span key="2" style={{ width: "5px", height: "5px", borderRadius: "50%", background: "#0a1628", display: "inline-block" }}></span>, <span key="3" style={{ width: "5px", height: "5px", borderRadius: "50%", background: "#0a1628", display: "inline-block" }}></span>]}
          </div>
        </button>
      </div>
    )
  }

  return (
    <div style={{ minHeight: "100vh", background: C.bg, color: C.text, fontFamily: "Georgia, serif" }}>
      <div style={navStyle}>
        <span style={{ color: C.gold, fontWeight: "bold", letterSpacing: "0.08em", fontSize: "1.1rem" }}>SURPLUS RECOVERY PRO</span>
        <div style={{ display: "flex", gap: "0.75rem" }}>
          <button onClick={() => openAuth("login")} style={{ padding: "0.35rem 1rem", border: "1px solid " + C.border, borderRadius: "3px", background: "none", color: C.light, cursor: "pointer", fontFamily: "Georgia, serif", fontSize: "0.82rem", letterSpacing: "0.05em" }}>LOG IN</button>
          <button onClick={() => openAuth("signup")} style={{ padding: "0.35rem 1rem", border: "none", borderRadius: "3px", background: C.gold, color: "#0a1628", fontWeight: "bold", cursor: "pointer", fontFamily: "Georgia, serif", fontSize: "0.82rem", letterSpacing: "0.05em" }}>GET STARTED</button>
        </div>
      </div>

      <div style={{ textAlign: "center", padding: "5rem 2rem 3.5rem", maxWidth: "860px", margin: "0 auto" }}>
        <div style={{ display: "inline-block", border: "1px solid " + C.gold, color: C.gold, padding: "0.3rem 1.2rem", fontSize: "0.72rem", letterSpacing: "0.2em", textTransform: "uppercase", marginBottom: "1.75rem" }}>Surplus Recovery Platform</div>
        <h1 style={{ fontSize: "2.8rem", fontWeight: "bold", color: "#fff", lineHeight: 1.2, margin: "0 0 1.25rem" }}>
          Recover Unclaimed Funds<br /><span style={{ color: C.gold }}>Faster and Smarter</span>
        </h1>
        <p style={{ fontSize: "1.05rem", color: C.light, maxWidth: "560px", margin: "1.25rem auto 2.25rem", lineHeight: 1.8 }}>
          Professional-grade tools, legal support, and county access for surplus fund recovery - trusted by attorneys, investors, and recovery specialists.
        </p>
        <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
          <button onClick={() => openAuth("signup")} style={{ padding: "0.8rem 2.2rem", background: C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", fontSize: "0.9rem" }}>START FREE TRIAL</button>
          <button onClick={() => document.getElementById("pricing").scrollIntoView({ behavior: "smooth" })} style={{ padding: "0.8rem 2.2rem", background: "transparent", color: C.light, border: "1px solid " + C.border, borderRadius: "3px", cursor: "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", fontSize: "0.9rem" }}>VIEW PRICING</button>
        </div>
      </div>

      <div style={{ display: "flex", justifyContent: "center", gap: "3.5rem", padding: "2.25rem 2rem", borderTop: "1px solid " + C.border, borderBottom: "1px solid " + C.border, flexWrap: "wrap" }}>
        {[{ n: "$2.4M+", l: "Funds Recovered" }, { n: "1,200+", l: "Claims Filed" }, { n: "48", l: "States Covered" }, { n: "98%", l: "Client Satisfaction" }].map(function(s) {
          return (
            <div key={s.l} style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2rem", fontWeight: "bold", color: C.gold, fontFamily: "Georgia, serif" }}>{s.n}</div>
              <div style={{ fontSize: "0.68rem", color: C.muted, textTransform: "uppercase", letterSpacing: "0.15em", marginTop: "0.2rem" }}>{s.l}</div>
            </div>
          )
        })}
      </div>

      <div id="pricing" style={{ maxWidth: "1080px", margin: "0 auto", padding: "4rem 2rem" }}>
        <div style={{ fontSize: "0.7rem", textAlign: "center", color: C.gold, textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "0.5rem" }}>Pricing Plans</div>
        <div style={{ fontSize: "1.9rem", fontWeight: "bold", textAlign: "center", color: "#fff", marginBottom: "0.6rem" }}>Simple, Transparent Pricing</div>
        <div style={{ textAlign: "center", color: C.light, marginBottom: "2.5rem", fontSize: "0.92rem" }}>Choose the plan that fits your recovery practice</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(270px, 1fr))", gap: "1.25rem" }}>
          {tiers.map(function(t) {
            return <PricingCard key={t.name} t={t} hoveredTier={hoveredTier} setHoveredTier={setHoveredTier} onGetStarted={() => openAuth("signup")} onCheckout={() => handleCheckout(t.priceId, "subscription")} />
          })}
        </div>
        <div style={{ background: C.card, border: "1px solid " + C.border, borderRadius: "4px", padding: "2rem", marginTop: "2rem" }}>
          <div style={{ fontSize: "1.2rem", fontWeight: "bold", color: "#fff", marginBottom: "0.3rem", fontFamily: "Georgia, serif" }}>Add-on Services</div>
          <div style={{ color: C.muted, fontSize: "0.83rem", marginBottom: "1.5rem" }}>Membership required</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))", gap: "0.85rem" }}>
            {addons.map(function(a) {
              return (
                <div key={a.name} style={{ background: C.bg, border: "1px solid " + C.border, borderRadius: "3px", padding: "0.9rem", cursor: "pointer" }}>
                  <div style={{ fontSize: "0.83rem", color: C.light, marginBottom: "0.35rem" }}>{a.name}</div>
                  <div style={{ fontSize: "1rem", color: C.gold, fontWeight: "bold" }}>{a.price}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div style={{ textAlign: "center", padding: "2rem", borderTop: "1px solid " + C.border, color: C.muted, fontSize: "0.75rem", letterSpacing: "0.08em" }}>
        2026 SURPLUSRECOVERYPRO - ALL RIGHTS RESERVED
      </div>

      {modal === "auth" && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 200, padding: "1rem" }} onClick={() => { setModal(null); setForgotSent(false) }}>
          <div style={{ background: C.card, border: "1px solid " + C.border, borderTop: "3px solid " + C.gold, borderRadius: "4px", padding: "2.25rem", width: "100%", maxWidth: "380px", position: "relative" }} onClick={function(e) { e.stopPropagation() }}>
            <button onClick={() => { setModal(null); setForgotSent(false) }} style={{ position: "absolute", top: "0.75rem", right: "1rem", background: "none", border: "none", color: C.muted, fontSize: "1.4rem", cursor: "pointer" }}>x</button>
            <div style={{ fontSize: "0.68rem", color: C.gold, textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "0.4rem" }}>SurplusRecoveryPro</div>
            {mode === "forgot" ? (
              <div>
                <div style={{ fontSize: "1.4rem", fontWeight: "bold", color: "#fff", marginBottom: "0.4rem", fontFamily: "Georgia, serif" }}>Reset Password</div>
                <div style={{ color: C.muted, fontSize: "0.83rem", marginBottom: "1.75rem" }}>Enter your email and we will send you a reset link</div>
                {forgotSent ? (
                  <div style={{ background: "rgba(34,197,94,0.1)", border: "1px solid " + C.green, borderRadius: "3px", padding: "0.75rem", fontSize: "0.83rem", color: C.green, marginBottom: "1rem" }}>Reset link sent! Check your email.</div>
                ) : (
                  <form onSubmit={handleForgot}>
                    {authError && <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid " + C.red, borderRadius: "3px", padding: "0.75rem", marginBottom: "1rem", fontSize: "0.83rem", color: C.red }}>{authError}</div>}
                    <input style={inputStyle} type="email" placeholder="Email Address" value={form.email} onChange={function(e) { setForm({ ...form, email: e.target.value }) }} required />
                    <button type="submit" disabled={loading} style={{ width: "100%", padding: "0.85rem", background: loading ? C.muted : C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: loading ? "not-allowed" : "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", textTransform: "uppercase" }}>
                      {loading ? "Sending..." : "Send Reset Link"}
                    </button>
                  </form>
                )}
                <div style={{ textAlign: "center", marginTop: "1.25rem", fontSize: "0.83rem", color: C.muted }}>
                  <span style={{ color: C.gold, cursor: "pointer" }} onClick={() => { setMode("login"); setAuthError(""); setForgotSent(false) }}>Back to Sign In</span>
                </div>
              </div>
            ) : (
              <div>
                <div style={{ fontSize: "1.4rem", fontWeight: "bold", color: "#fff", marginBottom: "0.4rem", fontFamily: "Georgia, serif" }}>{mode === "login" ? "Welcome Back" : "Create Account"}</div>
                <div style={{ color: C.muted, fontSize: "0.83rem", marginBottom: "1.75rem" }}>{mode === "login" ? "Sign in to your account" : "Start your free trial today"}</div>
                {authError && (
                  <div style={{ background: authError.includes("Check your email") ? "rgba(34,197,94,0.1)" : "rgba(239,68,68,0.1)", border: "1px solid " + (authError.includes("Check your email") ? C.green : C.red), borderRadius: "3px", padding: "0.75rem", marginBottom: "1rem", fontSize: "0.83rem", color: authError.includes("Check your email") ? C.green : C.red }}>
                    {authError}
                  </div>
                )}
                <form onSubmit={handleLogin}>
                  {mode === "signup" && <input style={inputStyle} placeholder="Full Name" value={form.name} onChange={function(e) { setForm({ ...form, name: e.target.value }) }} />}
                  <input style={inputStyle} type="email" placeholder="Email Address" value={form.email} onChange={function(e) { setForm({ ...form, email: e.target.value }) }} required />
                  <div style={{ position: "relative", marginBottom: "1rem" }}>
                    <input style={{ ...inputStyle, marginBottom: 0, paddingRight: "2.5rem" }} type={showPassword ? "text" : "password"} placeholder="Password" value={form.password} onChange={function(e) { setForm({ ...form, password: e.target.value }) }} required />
                    <span onClick={() => setShowPassword(!showPassword)} style={{ position: "absolute", right: "0.75rem", top: "50%", transform: "translateY(-50%)", cursor: "pointer", color: C.muted, fontSize: "0.75rem", userSelect: "none" }}>{showPassword ? "HIDE" : "SHOW"}</span>
                  </div>
                  {mode === "login" && (
                    <div style={{ textAlign: "right", marginBottom: "1rem" }}>
                      <span style={{ fontSize: "0.8rem", color: C.gold, cursor: "pointer" }} onClick={() => { setMode("forgot"); setAuthError("") }}>Forgot password?</span>
                    </div>
                  )}
                  <button type="submit" disabled={loading} style={{ width: "100%", padding: "0.85rem", background: loading ? C.muted : C.gold, color: "#0a1628", border: "none", borderRadius: "3px", fontWeight: "bold", cursor: loading ? "not-allowed" : "pointer", fontFamily: "Georgia, serif", letterSpacing: "0.08em", textTransform: "uppercase" }}>
                    {loading ? "Please wait..." : (mode === "login" ? "Sign In" : "Create Account")}
                  </button>
                </form>
                <div style={{ textAlign: "center", marginTop: "1.25rem", fontSize: "0.83rem", color: C.muted }}>
                  {mode === "login" ? "Don't have an account? " : "Already have an account? "}
                  <span style={{ color: C.gold, cursor: "pointer" }} onClick={() => { setMode(mode === "login" ? "signup" : "login"); setAuthError("") }}>
                    {mode === "login" ? "Sign up free" : "Sign in"}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
