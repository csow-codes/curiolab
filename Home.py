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
prof.setdefault("badges", [])
prof.setdefault("experiments_completed", 0)

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
    
    # Animated XP bar
    st.progress(min(prof["xp"] % 100, 100) / 100)
    st.caption(f"XP: {prof['xp']%100}/100 • Streak: {prof['streak_days']} days 🔥")
    
    # Achievement badges
    if prof.get("badges"):
        st.markdown("### 🏆 Badges")
        badge_html = "".join([f'<span class="badge">{badge}</span>' for badge in prof["badges"][:3]])
        st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔎 Quick links")
    try:
        st.page_link("pages/0_Get_Started.py", label="Get Started", icon="👩‍🔬")
        st.page_link("pages/1_Missions_Hub.py", label="Missions", icon="🧭")
        st.page_link("pages/5_Analysis_Lab.py", label="Analysis Lab", icon="📊")
    except Exception:
        st.caption("Pages will appear after setup.")

# ---------- Hero ----------
# Debug: Check if mascot exists
mascot_exists = os.path.exists("assets/dr_curio.png")
if not mascot_exists:
    mascot_exists = os.path.exists("dr_curio.png")
    mascot_path = "dr_curio.png" if mascot_exists else "assets/dr_curio.png"
else:
    mascot_path = "assets/dr_curio.png"

header_with_mascot(
    title="curiolab",
    subtitle="where curiosity becomes real research ✨",
    mascot_path=mascot_path,
    size_px=140,
)

# ---------- Live Stats Counter ----------
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="stats-counter">🌍 1,247</div><p style="text-align:center;color:#6b7c8a;">Scientists Worldwide</p>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stats-counter">🔬 {prof["experiments_completed"]}</div><p style="text-align:center;color:#6b7c8a;">Your Experiments</p>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stats-counter">⚡ {prof["xp"]}</div><p style="text-align:center;color:#6b7c8a;">Total XP</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Quick Experiment Button ----------
st.markdown('<div style="text-align:center;margin:32px 0;">', unsafe_allow_html=True)
if st.button("🚀 Try a 30-Second Experiment NOW!", key="quick_exp", use_container_width=False):
    experiments = [
        "💨 Blow on your hand with mouth open, then with lips pursed. Which feels cooler? Why?",
        "🌈 Look at a white surface through your fingers held close to your eye. See the diffraction?",
        "🔊 Hum and plug/unplug your ears. Notice how the sound changes!",
        "💧 Drop water on different surfaces. Which spreads most? That's surface tension!",
        "🌡️ Touch metal and wood. Same temp but metal feels colder. That's thermal conductivity!",
    ]
    st.info(random.choice(experiments))
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Daily challenge (interactive flip card) ----------
st.markdown("<br>", unsafe_allow_html=True)

daily_options = [
    ("📐 Measure temperature 3 times today", "💡 Tip: Check morning, noon, and evening. Notice the pattern?"),
    ("☁️ Observe cloud types for 10 minutes", "💡 Tip: Cumulus = fluffy, Stratus = flat layers, Cirrus = wispy!"),
    ("🍃 Sketch 3 different leaves you find", "💡 Tip: Look at the edges, veins, and shape. Are they symmetrical?"),
    ("🐝🦋 Count bees or butterflies for 10 minutes", "💡 Tip: Stay still and quiet. What flowers do they visit most?"),
]
random.seed(dt.date.today().toordinal())
daily, tip = random.choice(daily_options)

# Use session state for flip
if 'challenge_flipped' not in st.session_state:
    st.session_state.challenge_flipped = False

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(
        f"""
        <div class="daily-challenge">
            <h3 style="margin:0 0 12px 0;">🌞 Daily Challenge</h3>
            <p style="margin:0;font-size:1.05rem;font-weight:500;">{daily}</p>
            <p style="margin:12px 0 0 0;font-size:0.9rem;color:#8b7a3d;font-style:italic;">{tip if st.session_state.challenge_flipped else '💭 Click the button to reveal a tip!'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    if st.button("💡 Get Tip" if not st.session_state.challenge_flipped else "🎯 Got it!", key="flip_challenge"):
        st.session_state.challenge_flipped = not st.session_state.challenge_flipped
        st.rerun()

# ---------- Streak Calendar ----------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📅 Your Research Streak")
st.caption("Keep logging data every day to maintain your streak!")

# Simple 7-day streak visualization
today = dt.date.today()
streak_html = '<div class="streak-calendar">'
for i in range(6, -1, -1):
    day = today - dt.timedelta(days=i)
    is_active = i <= prof.get("streak_days", 0)
    day_class = "active" if is_active else "inactive"
    streak_html += f'<div class="streak-day {day_class}">{day.strftime("%a")[0]}</div>'
streak_html += '</div>'
st.markdown(streak_html, unsafe_allow_html=True)

# ---------- Missions (clean cards) ----------
st.markdown("<br><br>", unsafe_allow_html=True)
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

# ---------- Random Science Fact ----------
st.markdown("### 💡 Did You Know?")
facts = [
    "🦋 A butterfly's wings are actually transparent! The colors come from light reflecting off tiny scales.",
    "🌱 Plants can 'hear' water flowing underground and grow their roots toward it!",
    "⚡ Lightning is 5 times hotter than the surface of the Sun!",
    "🐝 Bees can recognize human faces and remember them for days!",
    "🌍 If you could fold a paper 42 times, it would reach the Moon!",
    "🔬 There are more bacteria in your body than stars in the Milky Way galaxy!",
    "🌈 You can never see a full rainbow - it's always a circle, but the ground blocks the bottom half!",
]
random.seed(dt.date.today().toordinal() + 1)  # Different seed than daily challenge
st.info(random.choice(facts))

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Science Buddy (chat) ----------
st.markdown("---")
st.subheader("🤖 Science Buddy")
st.caption("Ask simple questions and get friendly, accurate explanations.")

q = st.chat_input("Ask your Science Buddy (e.g., Why are plants green?)")
if q:
    # Try to get API key from Streamlit secrets first, then environment variable
    OPENAI = None
    try:
        if "OPENAI_API_KEY" in st.secrets:
            OPENAI = st.secrets["OPENAI_API_KEY"]
        elif hasattr(st.secrets, "OPENAI_API_KEY"):
            OPENAI = st.secrets.OPENAI_API_KEY
    except Exception:
        pass
    
    if not OPENAI:
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
            st.chat_message("assistant").write(f"Oops! {e}")
    else:
        # Fallback responses when no API key
        responses = {
            "green": "Great question! 🌿 Plants are green because of chlorophyll, a special pigment in their leaves. Chlorophyll absorbs red and blue light from the sun for photosynthesis, but reflects green light back to our eyes. That's why we see them as green!",
            "sky": "Awesome question! 🌤️ The sky is blue because of something called Rayleigh scattering. Sunlight is made of all colors, but blue light has shorter waves that scatter more when hitting air molecules. That scattered blue light reaches our eyes from all directions, making the sky look blue!",
            "rain": "Good thinking! 🌧️ Rain forms when water vapor in clouds condenses into droplets. As the droplets get bigger and heavier, gravity pulls them down to Earth. Temperature, air pressure, and humidity all work together to create rain!",
            "stars": "Amazing question! ⭐ Stars twinkle because their light passes through Earth's atmosphere, which is constantly moving. The moving air bends and bounces the light around, making stars appear to flicker. In space, stars don't twinkle at all!",
            "moon": "Great observation! 🌙 The Moon doesn't make its own light - it reflects light from the Sun! We see different moon phases because the Sun lights up different parts of the Moon as it orbits Earth. A full moon happens when the Sun lights up the whole side facing us!",
        }
        
        # Find best match
        q_lower = q.lower()
        response = None
        for keyword, answer in responses.items():
            if keyword in q_lower:
                response = answer
                break
        
        if not response:
            response = "That's a great science question! 🔬 I'm running in demo mode right now. To get AI-powered answers to all your questions, ask your teacher to add an OpenAI API key to the app settings. In the meantime, try asking about: plants being green, why the sky is blue, how rain forms, why stars twinkle, or why the moon glows!"
        
        st.chat_message("assistant").write(response)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Built with curiosity by Charlize S. ❤️✨")
