import streamlit as st, json, os, random, datetime as dt
from lang import t
from theme import apply_global_theme, header_with_mascot

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
apply_global_theme()

# ---------- sidebar avatar / XP ----------
with st.sidebar:
    st.markdown("### 🏠 Scientist Homebase")
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

# ---------- Hero with logo on Home ----------
header_with_mascot(
    title="🧪 CurioLab",
    subtitle="Where curiosity becomes real research ✨",
    mascot_path="assets/dr_curio.png",
    size_px=96,
)

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
