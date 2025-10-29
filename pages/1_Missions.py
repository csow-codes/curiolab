import streamlit as st, os, json, pandas as pd, datetime as dt, base64

st.set_page_config(page_title="Missions", page_icon="🧭", layout="wide")

def cute_box(text: str, bg="#e0f2fe"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #bfdbfe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

# CurioLab styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');
html, body, [class^="css"], p, li, span, div { 
  font-family: 'Poppins', system-ui, sans-serif; 
  font-weight: 300;
  color: #a4a4a4;
}
h1, h2, h3, h4, .hero h1, .hero h3, .card h3 { 
  font-family: 'Nunito', system-ui, sans-serif; 
  font-weight: 900;
  color: #7c9aa8;
}
.hero{background:linear-gradient(135deg,#e0f2fe 0%,#f0f9ff 60%,#ecfccb 100%);border-radius:28px;padding:42px 54px;margin-bottom:28px;text-align:center;box-shadow:0 8px 24px rgba(59,130,246,.18);border:2px solid #bfdbfe}
.hero h1{font-size:2.4rem;margin:0 0 8px}
.hero p{color:#a4a4a4;margin:6px 0 0 0;font-weight:300}
.logo-curio{animation:bounce 2s ease-in-out infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.card{background:#fff;border-radius:20px;border:2px solid #e2e8f0;padding:20px;box-shadow:0 4px 12px rgba(2,6,23,.06)}
.card h3{margin:0 0 8px;color:#7c9aa8}
</style>
""", unsafe_allow_html=True)

def count_rows(path): 
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

# Hero
logo_path = "avatars/curio_logo.png"
if os.path.exists(logo_path):
    _b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(f"""
    <div class='hero'>
      <div style='display:flex;align-items:center;justify-content:center;gap:16px;'>
        <img class='logo-curio' src='data:image/png;base64,{_b64}' style='width:68px;height:68px;border-radius:14px;'>
        <h1>CurioLab Missions</h1>
        <span style='font-size:2rem'>🧭</span>
      </div>
      <p>Pick a mission with <strong>Dr. Curio</strong> and earn XP by collecting real data!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='hero'>
      <div style='display:flex;align-items:center;justify-content:center;gap:16px;'>
        <span class='logo-curio' style='font-size:2.6rem'>🦫</span>
        <h1>CurioLab Missions</h1>
        <span style='font-size:2rem'>🧭</span>
      </div>
      <p>Pick a mission with <strong>Dr. Curio</strong> and earn XP by collecting real data!</p>
    </div>
    """, unsafe_allow_html=True)

# Progress
prof = {}
if os.path.exists("profile.json"):
    try: prof = json.load(open("profile.json","r"))
    except Exception: prof = {}
prof.setdefault("xp",0); prof.setdefault("streak_days",0)
px1,px2,px3 = st.columns(3)
with px1: st.metric("XP", f"{prof['xp']%100}/100")
with px2: st.metric("Streak", f"{prof['streak_days']} days")
with px3: st.caption("Complete any mission to gain +5 XP")

air_rows = count_rows("data/logs_air.csv")
seed_rows = count_rows("data/logs_seeds.csv")
pol_rows = count_rows("data/logs_pollinators.csv")

c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class='card' style='border-color:#93c5fd;background:linear-gradient(135deg,#dbeafe 0%,#e0f2fe 100%);'>
      <h3 style='color:#1e40af'>🌤️ Air & Weather</h3>
      <p style='margin:0;color:#334155'>Observations: <strong>""" + str(air_rows) + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Air_Quality.py", label="Start Mission →", icon="🌤️")
with c2:
    st.markdown("""
    <div class='card' style='border-color:#86efac;background:linear-gradient(135deg,#ecfccb 0%,#f0fdf4 100%);'>
      <h3 style='color:#166534'>🌱 Seeds & Growth</h3>
      <p style='margin:0;color:#334155'>Observations: <strong>""" + str(seed_rows) + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Seeds_Growth.py", label="Start Mission →", icon="🌱")
with c3:
    st.markdown("""
    <div class='card' style='border-color:#fbbf24;background:linear-gradient(135deg,#fef3c7 0%,#fef9e7 100%);'>
      <h3 style='color:#92400e'>🐝 Pollinator Patrol</h3>
      <p style='margin:0;color:#334155'>Observations: <strong>""" + str(pol_rows) + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Pollinator_Patrol.py", label="Start Mission →", icon="🐝")

st.markdown("---")
st.subheader("🎓 Teacher & Coach")
colA, colB = st.columns(2)
with colA:
    st.write("Download CSV logs:")
    if os.path.exists("data/logs_air.csv"): st.download_button("⬇️ Air & Weather CSV", data=open("data/logs_air.csv","rb").read(), file_name="logs_air.csv")
    if os.path.exists("data/logs_seeds.csv"): st.download_button("⬇️ Seeds & Growth CSV", data=open("data/logs_seeds.csv","rb").read(), file_name="logs_seeds.csv")
    if os.path.exists("data/logs_pollinators.csv"): st.download_button("⬇️ Pollinators CSV", data=open("data/logs_pollinators.csv","rb").read(), file_name="logs_pollinators.csv")
with colB:
    st.write("Quick feedback (1–2 questions)")
    ease = st.slider("How easy was LearnLab to use?", 1, 5, 4)
    conf = st.slider("Do the charts make sense?", 1, 5, 4)
    msg  = st.text_input("One thing to improve", "")
    if st.button("Submit feedback"):
        os.makedirs("data", exist_ok=True)
        with open("data/feedback.csv","a") as f:
            f.write(f"{str(dt.date.today())},{ease},{conf},{msg}\n")
        st.success("Thanks! ✨")
    if os.path.exists("data/feedback.csv"):
        fb = pd.read_csv("data/feedback.csv", header=None, names=["date","ease","conf","msg"])
        st.caption(f"Feedback so far — ease: {fb['ease'].mean():.1f}/5, understanding: {fb['conf'].mean():.1f}/5 (n={len(fb)})")