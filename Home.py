import streamlit as st, json, os, random, datetime as dt
from lang import t

st.set_page_config(page_title="LearnLab — Home", page_icon="🧪", layout="wide")

# ---------- load profile ----------
prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json","r"))
    except Exception:
        prof = {}
# defaults
prof.setdefault("name","Scientist")
prof.setdefault("language","English")
prof.setdefault("xp", 0)
prof.setdefault("streak_days", 0)
prof.setdefault("last_log_date", None)

LANG = prof["language"]

# ---------- CSS: animated hero + cute UI ----------
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');

/* Global typography */
html, body, [class^="css"]  {
  font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif;
  color: #a4a4a4; /* Poppins Light gray */
}
h1, h2, h3, .hero h1, .hero h3 { 
  font-family: 'Nunito', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif; 
  font-weight: 900; /* Extra Bold */
  color: #7c9aa8; /* header color */
}
p, li, span, div { color: #a4a4a4; }

/* Hero block visuals remain */
.hero{background:linear-gradient(135deg,#f8f4ff 0%,#fffdfc 100%);border-radius:20px;padding:40px 60px;margin-bottom:28px;text-align:center;box-shadow:0 0 10px rgba(167,139,250,.15)}
.hero h1{font-size:2.6rem;margin:0 0 8px}
.hero h3{font-weight:400;font-size:1.2rem;margin:0}
.floaty{animation:float 4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.card:hover{transform:scale(1.01)}
</style>
""", unsafe_allow_html=True)

# ---------- sidebar avatar / XP ----------
with st.sidebar:
    st.markdown("### 🏠 Scientist Homebase")
    # Dr. Curio logo (place your image at avatars/dr_curio.png or assets/dr_curio.png)
    for _logo_path in ("avatars/dr_curio.png", "assets/dr_curio.png"):
        if os.path.exists(_logo_path):
            st.image(_logo_path, width=140, caption="Dr. Curio")
            break
    if prof.get("avatar") and os.path.exists(prof["avatar"]):
        st.image(prof["avatar"], width=120, caption=prof.get("name","Scientist"))
    st.progress(min(prof["xp"] % 100, 100))
    st.caption(f"XP: {prof['xp']%100}/100 • Streak: {prof['streak_days']} days")

    st.markdown("### 🔎 Quick links")
    try:
        st.page_link("pages/0_Get_Started.py", label="Get Started", icon="👩‍🔬")
        st.page_link("pages/1_Missions_Hub.py", label="Missions", icon="🧭")
        st.page_link("pages/5_Analysis_Lab.py", label="Analysis Lab", icon="📊")
    except Exception:
        st.write("Pages will appear after you rename/add them.")

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <h1>🧪 LearnLab</h1>
  <h3>Where curiosity becomes real research ✨</h3>
  <p style="color:#555;margin-top:6px;">Turn any classroom or backyard into a mini research lab.</p>
  <img class="floaty" src="https://cdn-icons-png.flaticon.com/512/4148/4148460.png" width="60">
  <img class="floaty" src="https://cdn-icons-png.flaticon.com/512/766/766513.png" width="60">
</div>
""", unsafe_allow_html=True)

# ---------- Daily challenge ----------
daily_options = [
    "Measure temperature 3 times today 🌡️",
    "Observe cloud types for 10 minutes ☁️",
    "Sketch 3 leaves you find 🍃",
    "Count bees or butterflies for 10 minutes 🐝🦋",
]
random.seed(dt.date.today().toordinal())
daily = random.choice(daily_options)
st.markdown(f"### 🌞 Daily Challenge\n{daily}")

# ---------- Missions (cards) ----------
st.markdown(f"### 🧭 {t('Missions', LANG)}")
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("#### 🌤️ Air & Weather")
    st.write("Log temperature, rainfall, and PM2.5. Get an AI mini report.")
    st.page_link("pages/2_Air_Quality.py", label=t("Open module →", LANG), icon="🌤️")
with c2:
    st.markdown("#### 🌱 Seeds & Growth")
    st.write("Track plant height and discover growth patterns.")
    st.page_link("pages/3_Seeds_Growth.py", label=t("Open module →", LANG), icon="🌱")
with c3:
    st.markdown("#### 🐝 Pollinator Patrol")
    st.write("Count bees & butterflies to study biodiversity.")
    st.page_link("pages/4_Pollinator_Patrol.py", label=t("Open module →", LANG), icon="🐝")

st.markdown("---")

# ---------- Science Buddy (chat) ----------
st.subheader("🤖 Science Buddy")
st.caption("Ask simple questions and get friendly, accurate explanations.")
q = st.chat_input("Ask your Science Buddy (e.g., Why are plants green?)")
if q:
    OPENAI = os.getenv("OPENAI_API_KEY")
    if OPENAI:
        try:
            import openai
            openai.api_key = OPENAI
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You are a friendly science buddy for learners age 10–14. Keep it accurate, simple, curious, with emojis."},
                    {"role":"user","content":q}
                ],
                temperature=0.3, max_tokens=300
            )
            st.chat_message("assistant").write(resp.choices[0].message.content)
        except Exception as e:
            st.chat_message("assistant").write(f"(AI unavailable: {e}) Try again later!")
    else:
        st.chat_message("assistant").write("Add OPENAI_API_KEY to enable the Science Buddy.")

st.markdown("---")
st.caption("Built by Charlize S., another fellow scientist ❤️")
