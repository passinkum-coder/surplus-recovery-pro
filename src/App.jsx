
import { useState } from "react"

const C = {
  bg: "#0a1628", card: "#0f2040", border: "#1a3058",
  gold: "#c9a84c", text: "#e8e0d0", muted: "#6b7a8d",
  light: "#a0aec0", green: "#22c55e", red: "#ef4444",
  purple: "#818cf8", nav: "#071020"
}

const claims = [
  { id:"SRP-001", owner:"James Wilson", county:"Cook County, IL", amount:"$12,400", status:"Active", date:"Mar 1, 2026" },
  { id:"SRP-002", owner:"Maria Garcia", county:"Harris County, TX", amount:"$8,750", status:"Pending", date:"Feb 28, 2026" },
  { id:"SRP-003", owner:"Robert Chen", county:"LA County, CA", amount:"$31,200", status:"Filed", date:"Feb 25, 2026" },
  { id:"SRP-004", owner:"Lisa Thompson", county:"Maricopa, AZ", amount:"$5,900", status:"Complete", date:"Feb 20, 2026" },
]
const tiers = [
  { name:"Basic", price:"$49", features:["Single county access","Owner contract templates","Basic surplus search tools","Claim status tracking","Email support"] },
  { name:"Professional", price:"$149", featured:true, features:["Multi-county access (up to 5)","Owner contract templates","Document filing guides","Claim status tracking","Skip tracing (10/mo)","Priority email support","County auction alerts"] },
  { name:"Premium", price:"$349", features:["Unlimited county access","Lawyer consultations (2/mo)","Skip tracing (unlimited)","Automated owner outreach","Court filing assistance","Heir research tools","Lead list exports","Dedicated account manager"] },
]
const addons = [
  {name:"Extra County Access",price:"$19/mo"},{name:"Lawyer Consultation",price:"$99/session"},
  {name:"Skip Trace Search",price:"$12/search"},{name:"Document Notarization",price:"$29/doc"},
  {name:"Heir Research Report",price:"$79/report"},{name:"Done-For-You Filing",price:"$199/claim"},
  {name:"Lead List Export",price:"$49/export"},{name:"Training Course",price:"$299 one-time"},
]

function Badge({status}) {
  const map = {Active:{bg:"rgba(201,168,76,0.15)",c:"#c9a84c"},Pending:{bg:"rgba(240,180,41,0.15)",c:"#f0b429"},Filed:{bg:"rgba(129,140,248,0.15)",c:"#818cf8"},Complete:{bg:"rgba(34,197,94,0.15)",c:"#22c55e"}}
  const s = map[status]||map.Active
  return <span style={{background:s.bg,color:s.c,padding:"0.2rem 0.6rem",borderRadius:"3px",fontSize:"0.72rem",fontWeight:"bold",letterSpacing:"0.05em",textTransform:"uppercase"}}>{status}</span>
}

export default function App() {
  const [page, setPage] = useState("home")
  const [modal, setModal] = useState(null)
  const [mode, setMode] = useState("login")
  const [user, setUser] = useState(null)
  const [form, setForm] = useState({name:"",email:"",password:""})

  const nav = {display:"flex",justifyContent:"space-between",alignItems:"center",padding:"0 2rem",height:"58px",background:C.nav,borderBottom:`3px solid ${C.gold}`,position:"sticky",top:0,zIndex:100}
  const inp = {width:"100%",padding:"0.7rem",background:"#071020",border:`1px solid ${C.border}`,borderRadius:"3px",color:C.text,fontSize:"0.9rem",marginBottom:"1rem",boxSizing:"border-box",fontFamily:"Georgia,serif",outline:"none"}

  const login = (e) => {
    e.preventDefault()
    setUser({name:form.name||"Gary",tier:"Professional"})
    setModal(null)
    setPage("dashboard")
  }

  if (page==="dashboard") return (
    <div style={{minHeight:"100vh",background:C.bg,color:C.text,fontFamily:"Georgia,serif"}}>
      <div style={nav}>
        <span style={{color:C.gold,fontWeight:"bold",letterSpacing:"0.08em",cursor:"pointer",fontSize:"1.1rem"}} onClick={()=>setPage("home")}>SURPLUS RECOVERY PRO</span>
        <div style={{display:"flex",gap:"1.5rem",alignItems:"center"}}>
          <span style={{color:C.muted,fontSize:"0.82rem",letterSpacing:"0.05em"}}>{user?.name?.toUpperCase()} · <span style={{color:C.gold}}>PROFESSIONAL</span></span>
          <button onClick={()=>{setUser(null);setPage("home")}} style={{padding:"0.35rem 0.9rem",border:`1px solid ${C.border}`,borderRadius:"3px",background:"none",color:C.light,cursor:"pointer",fontFamily:"Georgia,serif",fontSize:"0.8rem",letterSpacing:"0.05em"}}>SIGN OUT</button>
        </div>
      </div>
      <div style={{padding:"2rem 2.5rem"}}>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:"2rem",flexWrap:"wrap",gap:"1rem"}}>
          <div>
            <div style={{fontSize:"1.5rem",fontWeight:"bold",color:"#fff",marginBottom:"0.25rem"}}>Welcome back, {user?.name}</div>
            <div style={{color:C.muted,fontSize:"0.8rem",letterSpacing:"0.08em",textTransform:"uppercase"}}>Surplus Recovery Dashboard · Professional Plan</div>
          </div>
          <button style={{padding:"0.65rem 1.4rem",background:C.gold,color:"#0a1628",border:"none",borderRadius:"3px",fontWeight:"bold",cursor:"pointer",fontFamily:"Georgia,serif",letterSpacing:"0.06em",fontSize:"0.85rem"}}>+ NEW CLAIM</button>
        </div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(190px,1fr))",gap:"1.25rem",marginBottom:"2rem"}}>
          {[{l:"Active Claims",v:"4",s:"+2 this month",c:C.gold},{l:"Total Recovered",v:"$58,250",s:"↑ 18% vs last month",c:C.green},{l:"Counties Tracked",v:"3",s:"5 max on your plan",c:C.purple},{l:"Pending Actions",v:"2",s:"Requires attention",c:C.red}].map(x=>(
            <div key={x.l} style={{background:C.card,borderTop:`3px solid ${x.c}`,border:`1px solid ${C.border}`,borderRadius:"4px",padding:"1.4rem"}}>
              <div style={{fontSize:"0.68rem",color:C.muted,textTransform:"uppercase",letterSpacing:"0.13em",marginBottom:"0.6rem"}}>{x.l}</div>
              <div style={{fontSize:"1.9rem",fontWeight:"bold",color:"#fff",marginBottom:"0.2rem"}}>{x.v}</div>
              <div style={{fontSize:"0.78rem",color:x.c}}>{x.s}</div>
            </div>
          ))}
        </div>
        <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:"4px",overflow:"hidden"}}>
          <div style={{padding:"1rem 1.5rem",borderBottom:`1px solid ${C.border}`,display:"flex",justifyContent:"space-between",alignItems:"center"}}>
            <span style={{fontWeight:"bold",color:"#fff",fontSize:"0.85rem",textTransform:"uppercase",letterSpacing:"0.08em"}}>Recent Claims</span>
            <span style={{fontSize:"0.78rem",color:C.gold,cursor:"pointer",letterSpacing:"0.05em"}}>VIEW ALL →</span>
          </div>
          <table style={{width:"100%",borderCollapse:"collapse"}}>
            <thead><tr style={{background:"#071020"}}>{["Claim ID","Owner","County","Amount","Status","Date"].map(h=><th key={h} style={{padding:"0.7rem 1.25rem",textAlign:"left",fontSize:"0.68rem",color:C.muted,textTransform:"uppercase",letterSpacing:"0.12em",borderBottom:`1px solid ${C.border}`}}>{h}</th>)}</tr></thead>
            <tbody>{claims.map((r,i)=>(
              <tr key={r.id} style={{background:i%2===0?"transparent":"rgba(255,255,255,0.015)"}}>
                <td style={{padding:"0.9rem 1.25rem",color:C.gold,fontSize:"0.88rem",fontWeight:"bold"}}>{r.id}</td>
                <td style={{padding:"0.9rem 1.25rem",color:C.text,fontSize:"0.88rem"}}>{r.owner}</td>
                <td style={{padding:"0.9rem 1.25rem",color:C.light,fontSize:"0.82rem"}}>{r.county}</td>
                <td style={{padding:"0.9rem 1.25rem",color:"#fff",fontWeight:"bold",fontSize:"0.88rem"}}>{r.amount}</td>
                <td style={{padding:"0.9rem 1.25rem"}}><Badge status={r.status}/></td>
                <td style={{padding:"0.9rem 1.25rem",color:C.muted,fontSize:"0.82rem"}}>{r.date}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </div>
    </div>
  )

  return (
    <div style={{minHeight:"100vh",background:C.bg,color:C.text,fontFamily:"Georgia,serif"}}>
      <div style={nav}>
        <span style={{color:C.gold,fontWeight:"bold",letterSpacing:"0.08em",fontSize:"1.1rem"}}>SURPLUS RECOVERY PRO</span>
        <div style={{display:"flex",gap:"0.75rem"}}>
          <button onClick={()=>{setMode("login");setModal("auth")}} style={{padding:"0.35rem 1rem",border:`1px solid ${C.border}`,borderRadius:"3px",background:"none",color:C.light,cursor:"pointer",fontFamily:"Georgia,serif",fontSize:"0.82rem",letterSpacing:"0.05em"}}>LOG IN</button>
          <button onClick={()=>{setMode("signup");setModal("auth")}} style={{padding:"0.35rem 1rem",border:"none",borderRadius:"3px",background:C.gold,color:"#0a1628",fontWeight:"bold",cursor:"pointer",fontFamily:"Georgia,serif",fontSize:"0.82rem",letterSpacing:"0.05em"}}>GET STARTED</button>
        </div>
      </div>

      <div style={{textAlign:"center",padding:"5rem 2rem 3.5rem",maxWidth:"860px",margin:"0 auto"}}>
        <div style={{display:"inline-block",border:`1px solid ${C.gold}`,color:C.gold,padding:"0.3rem 1.2rem",fontSize:"0.72rem",letterSpacing:"0.2em",textTransform:"uppercase",marginBottom:"1.75rem"}}>Surplus Recovery Platform</div>
        <h1 style={{fontSize:"2.8rem",fontWeight:"bold",color:"#fff",lineHeight:1.2,marginBottom:"1.25rem",margin:"0 0 1.25rem"}}>Recover Unclaimed Funds<br/><span style={{color:C.gold}}>Faster & Smarter</span></h1>
        <p style={{fontSize:"1.05rem",color:C.light,maxWidth:"560px",margin:"1.25rem auto 2.25rem",lineHeight:1.8}}>Professional-grade tools, legal support, and county access for surplus fund recovery — trusted by attorneys, investors, and recovery specialists.</p>
        <div style={{display:"flex",gap:"1rem",justifyContent:"center",flexWrap:"wrap"}}>
          <button onClick={()=>{setMode("signup");setModal("auth")}} style={{padding:"0.8rem 2.2rem",background:C.gold,color:"#0a1628",border:"none",borderRadius:"3px",fontWeight:"bold",cursor:"pointer",fontFamily:"Georgia,serif",letterSpacing:"0.08em",fontSize:"0.9rem"}}>START FREE TRIAL</button>
          <button style={{padding:"0.8rem 2.2rem",background:"transparent",color:C.light,border:`1px solid ${C.border}`,borderRadius:"3px",cursor:"pointer",fontFamily:"Georgia,serif",letterSpacing:"0.08em",fontSize:"0.9rem"}}>VIEW PRICING ↓</button>
        </div>
      </div>

      <div style={{display:"flex",justifyContent:"center",gap:"3.5rem",padding:"2.25rem 2rem",borderTop:`1px solid ${C.border}`,borderBottom:`1px solid ${C.border}`,flexWrap:"wrap"}}>
        {[{n:"$2.4M+",l:"Funds Recovered"},{n:"1,200+",l:"Claims Filed"},{n:"48",l:"States Covered"},{n:"98%",l:"Client Satisfaction"}].map(s=>(
          <div key={s.l} style={{textAlign:"center"}}>
            <div style={{fontSize:"2rem",fontWeight:"bold",color:C.gold,fontFamily:"Georgia,serif"}}>{s.n}</div>
            <div style={{fontSize:"0.68rem",color:C.muted,textTransform:"uppercase",letterSpacing:"0.15em",marginTop:"0.2rem"}}>{s.l}</div>
          </div>
        ))}
      </div>

      <div style={{maxWidth:"1080px",margin:"0 auto",padding:"4rem 2rem"}}>
        <div style={{fontSize:"0.7rem",textAlign:"center",color:C.gold,textTransform:"uppercase",letterSpacing:"0.2em",marginBottom:"0.5rem"}}>Pricing Plans</div>
        <div style={{fontSize:"1.9rem",fontWeight:"bold",textAlign:"center",color:"#fff",marginBottom:"0.6rem"}}>Simple, Transparent Pricing</div>
        <div style={{textAlign:"center",color:C.light,marginBottom:"2.5rem",fontSize:"0.92rem"}}>Choose the plan that fits your recovery practice</div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(270px,1fr))",gap:"1.25rem"}}>
          {tiers.map(t=>(
            <div key={t.name} style={{background:C.card,borderTop:`3px solid ${t.featured?C.gold:C.border}`,border:`1px solid ${t.featured?C.gold:C.border}`,borderRadius:"4px",padding:"1.75rem",position:"relative"}}>
              {t.featured&&<div style={{position:"absolute",top:"-11px",left:"50%",transform:"translateX(-50%)",background:C.gold,color:"#0a1628",padding:"0.18rem 0.9rem",fontSize:"0.68rem",fontWeight:"bold",letterSpacing:"0.1em",textTransform:"uppercase",whiteSpace:"nowrap"}}>MOST POPULAR</div>}
              <div style={{fontSize:"0.75rem",fontWeight:"bold",color:C.muted,textTransform:"uppercase",letterSpacing:"0.15em",marginBottom:"0.6rem"}}>{t.name}</div>
              <div style={{fontSize:"2.8rem",fontWeight:"bold",color:"#fff",fontFamily:"Georgia,serif",marginBottom:"0.2rem"}}>{t.price}</div>
              <div style={{fontSize:"0.75rem",color:C.muted,marginBottom:"1.5rem",letterSpacing:"0.05em"}}>PER MONTH</div>
              <ul style={{listStyle:"none",padding:0,margin:"0 0 1.75rem"}}>
                {t.features.map(f=><li key={f} style={{display:"flex",gap:"0.6rem",padding:"0.42rem 0",fontSize:"0.85rem",color:C.light,borderBottom:`1px solid ${C.border}`}}><span style={{color:C.gold,flexShrink:0}}>✓</span>{f}</li>)}
              </ul>
              <button onClick={()=>{setMode("signup");setModal("auth")}} style={{width:"100%",padding:"0.8rem",borderRadius:"3px",border:t.featured?"none":`1px solid ${C.border}`,background:t.featured?C.gold:"transparent",color:t.featured?"#0a1628":C.light,fontWeight:"bold",cursor:"pointer",fontFamily:"Georgia,serif",letterSpacing:"0.07em",fontSize:"0.82rem",textTransform:"uppercase"}}>Get Started</button>
            </div>
          ))}
        </div>

        <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:"4px",padding:"2rem",marginTop:"2rem"}}>
          <div style={{fontSize:"1.2rem",fontWeight:"bold",color:"#fff",marginBottom:"0.3rem",fontFamily:"Georgia,serif"}}>À La Carte Services</div>
          <div style={{color:C.muted,fontSize:"0.83rem",marginBottom:"1.5rem"}}>Add only what you need — no subscription required</div>
          <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(190px,1fr))",gap:"0.85rem"}}>
            {addons.map(a=>(
              <div key={a.name} style={{background:C.bg,border:`1px solid ${C.border}`,borderRadius:"3px",padding:"0.9rem",cursor:"pointer"}}>
                <div style={{fontSize:"0.83rem",color:C.light,marginBottom:"0.35rem"}}>{a.name}</div>
                <div style={{fontSize:"1rem",color:C.gold,fontWeight:"bold"}}>{a.price}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{textAlign:"center",padding:"2rem",borderTop:`1px solid ${C.border}`,color:C.muted,fontSize:"0.75rem",letterSpacing:"0.08em"}}>
        © 2026 SURPLUSRECOVERYPRO · ALL RIGHTS RESERVED
      </div>

      {modal==="auth"&&(
        <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,0.85)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:200,padding:"1rem"}} onClick={()=>setModal(null)}>
          <div style={{background:C.card,border:`1px solid ${C.border}`,borderTop:`3px solid ${C.gold}`,borderRadius:"4px",padding:"2.25rem",width:"100%",maxWidth:"380px",position:"relative"}} onClick={e=>e.stopPropagation()}>
            <button onClick={()=>setModal(null)} style={{position:"absolute",top:"0.75rem",right:"1rem",background:"none",border:"none",color:C.muted,fontSize:"1.4rem",cursor:"pointer"}}>×</button>
            <div style={{fontSize:"0.68rem",color:C.gold,textTransform:"uppercase",letterSpacing:"0.2em",marginBottom:"0.4rem"}}>SurplusRecoveryPro</div>
            <div style={{fontSize:"1.4rem",fontWeight:"bold",color:"#fff",marginBottom:"0.4rem",fontFamily:"Georgia,serif"}}>{mode==="login"?"Welcome Back":"Create Account"}</div>
            <div style={{color:C.muted,fontSize:"0.83rem",marginBottom:"1.75rem"}}>{mode==="login"?"Sign in to your account":"Start your free trial today"}</div>
            <form onSubmit={login}>
              {mode==="signup"&&<input style={inp} placeholder="Full Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>}
              <input style={inp} type="email" placeholder="Email Address" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required/>
              <input style={inp} type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} required/>
              <button type="submit" style={{width:"100%",padding:"0.85rem",background:C.gold,color:"#0a1628",border:"none",borderRadius:"3px",fontWeight:"bold",cursor:"pointer",fontFamily:"Georgia,serif",letterSpacing:"0.08em",textTransform:"uppercase"}}>
                {mode==="login"?"Sign In":"Create Account"}
              </button>
            </form>
            <div style={{textAlign:"center",marginTop:"1.25rem",fontSize:"0.83rem",color:C.muted}}>
              {mode==="login"?"Don't have an account? ":"Already have an account? "}
              <span style={{color:C.gold,cursor:"pointer"}} onClick={()=>setMode(mode==="login"?"signup":"login")}>{mode==="login"?"Sign up free":"Sign in"}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

