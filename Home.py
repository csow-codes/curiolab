import streamlit as st, json, os, random, datetime as dt
from lang import t
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="CurioLab — Home", page_icon="🧪", layout="wide")

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

# ---------- CSS ----------
apply_global_theme()

# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### 🏠 Scientist Homebase")
    if prof.get("avatar") and os.path.exists(prof["avatar"]):
        st.image(prof["avatar"], width=100, caption=prof.get("name","Scientist"))
    else:
        st.markdown(f"**{prof.get('name','Scientist')}**")
    
    st.progress(min(prof["xp"] % 100, 100) / 100)
    st.caption(f"XP: {prof['xp']%100}/100 • Streak: {prof['streak_days']} days")

    st.markdown("---")
    st.markdown("### 🔎 Quick links")
    try:
        st.page_link("pages/0_Get_Started.py", label="Get Started", icon="👩‍🔬")
        st.page_link("pages/1_Missions_Hub.py", label="Missions", icon="🧭")
        st.page_link("pages/5_Analysis_Lab.py", label="Analysis Lab", icon="📊")
    except Exception:
        st.caption("Pages will appear after setup.")

# ---------- Hero ----------
header_with_mascot(
    title="curiolab",
    subtitle="where curiosity becomes real research ✨",
    mascot_path="assets/dr_curio.png",
    size_px=140,
)

# ---------- Daily challenge (styled box) ----------
st.markdown("<br>", unsafe_allow_html=True)

daily_options = [
    "📐 Measure temperature 3 times today",
    "☁️ Observe cloud types for 10 minutes",
    "🍃 Sketch 3 different leaves you find",
    "🐝🦋 Count bees or butterflies for 10 minutes",
]
random.seed(dt.date.today().toordinal())
daily = random.choice(daily_options)

st.markdown(
    f"""
    <div class="daily-challenge">
        <h3 style="margin:0 0 12px 0;">🌞 Daily Challenge</h3>
        <p style="margin:0;font-size:1.05rem;">{daily}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Missions (clean cards) ----------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### 🧭 {t('Missions', LANG)}")
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🌤️ Air & Weather</h4>
            <p style="margin:0 0 16px 0;font-size:0.95rem;">Log temperature, rainfall, and PM2.5. Get an AI mini report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Air_Quality.py", label=t("Open module →", LANG), icon="🌤️")

with c2:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🌱 Seeds & Growth</h4>
            <p style="margin:0 0 16px 0;font-size:0.95rem;">Track plant height and discover growth patterns.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Seeds_Growth.py", label=t("Open module →", LANG), icon="🌱")

with c3:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🐝 Pollinator Patrol</h4>
            <p style="margin:0 0 16px 0;font-size:0.95rem;">Count bees & butterflies to study biodiversity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/4_Pollinator_Patrol.py", label=t("Open module →", LANG), icon="🐝")

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------- Science Buddy (chat) ----------
st.markdown("---")
st.subheader("🤖 Science Buddy")
st.caption("Ask simple questions and get friendly, accurate explanations.")

OPENAI = os.getenv("OPENAI_API_KEY")

if not OPENAI:
    st.info("💡 Add your `OPENAI_API_KEY` to Streamlit secrets to enable the Science Buddy chat!")
else:
    q = st.chat_input("Ask your Science Buddy (e.g., Why are plants green?)")
    if q:
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
            st.chat_message("assistant").write(f"Oops! {e}")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Built with curiosity by Charlize S. ❤️✨")
