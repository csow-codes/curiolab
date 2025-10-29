import streamlit as st, os, json, pandas as pd, datetime as dt, base64
from theme import apply_global_theme, header_with_mascot
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Missions", page_icon="🧭", layout="wide")
apply_global_theme()
header_with_mascot("CurioLab Missions", "Pick a mission and earn XP! ")
apply_global_theme()

def cute_box(text: str, bg="#e0f2fe"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #bfdbfe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

st.markdown("""
<style>
.hero{background:linear-gradient(135deg,#e8f3f8 0%,#f6fbff 60%,#ffffff 100%);border-radius:24px;padding:36px 44px;margin-bottom:20px;text-align:center;box-shadow:0 8px 24px rgba(124,154,168,.18);border:1px solid #dce9f0}
.card{background:#f6f9fb;border-radius:16px;border:1px solid #e2e8f0;padding:20px;box-shadow:0 4px 12px rgba(2,6,23,.04)}
.card h3{margin:0 0 8px}
</style>
""", unsafe_allow_html=True)

def count_rows(path): 
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

# Header
header_with_mascot("CurioLab Missions", "Pick a mission with Dr. Curio and earn XP!", mascot_path="assets/dr_curio.png", size_px=76)

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