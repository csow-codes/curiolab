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
    st.markdown('<div class="stats-counter">🌍 1,247</div><p style="text-align:center;color:#6b7c8a;font-size:0.85rem;">Scientists Worldwide<br><span style="font-size:0.75rem;opacity:0.7;">(Demo data)</span></p>', unsafe_allow_html=True)
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

# ---------- Recent Discoveries Carousel ----------
st.markdown("### 🔬 Recent Discoveries")
st.caption("See what other scientists are discovering! (Example data for demo)")

discovery_tabs = st.tabs(["🌍 Today", "📅 This Week", "🏆 Top Rated"])

with discovery_tabs[0]:
    discoveries_today = [
        "🌡️ **Sarah M.** discovered temperature drops 5°C at sunset in Phoenix!",
        "🌱 **Alex K.** observed their bean plant grew 3cm in just 2 days!",
        "🐝 **Jordan T.** counted 47 bees visiting lavender in 10 minutes!",
    ]
    for disc in discoveries_today:
        st.markdown(f"- {disc}")

with discovery_tabs[1]:
    discoveries_week = [
        "🌧️ **Emma L.** tracked rainfall patterns and predicted the next storm!",
        "🦋 **Liam P.** identified 8 different butterfly species in their backyard!",
        "☁️ **Mia R.** documented all 10 cloud types in a single week!",
    ]
    for disc in discoveries_week:
        st.markdown(f"- {disc}")

with discovery_tabs[2]:
    discoveries_top = [
        "⭐ **Chris B.** created a complete weather station from recycled materials!",
        "⭐ **Taylor N.** grew plants in 5 different conditions to test photosynthesis!",
        "⭐ **Morgan S.** built a bee hotel and documented 12 different species!",
    ]
    for disc in discoveries_top:
        st.markdown(f"- {disc}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Challenge Friends Feature ----------
st.markdown("### 🤝 Challenge a Friend")
col1, col2 = st.columns([2, 1])
with col1:
    st.text_input("Enter friend's email", placeholder="scientist@curiolab.org", key="friend_email")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Send Challenge", key="send_challenge"):
        st.success("Challenge sent! 🎯")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Leaderboard Preview ----------
st.markdown("### 🏆 Top Scientists This Week")
st.caption("Example leaderboard - compete with scientists around the world!")

# Use columns for cleaner display
lb_data = [
    ("🥇", "Emma L.", 450, "🔥 12 day streak"),
    ("🥈", "Alex K.", 380, "🌱 Plant Expert"),
    ("🥉", "Jordan T.", 320, "🐝 Bee Whisperer"),
    ("4️⃣", "You!", prof["xp"], f"💪 {prof['streak_days']} day streak"),
    ("5️⃣", "Sarah M.", 280, "🌡️ Weather Pro"),
]

# Create a container with clean styling
st.markdown("""
<style>
.leaderboard-container {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(90,138,158,0.08);
}
.lb-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
}
.lb-row.highlight {
    background: linear-gradient(135deg,#fff9e6 0%,#fffef5 100%);
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

for rank, name, xp, badge in lb_data:
    if name == "You!":
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff9e6 0%,#fffef5 100%);border-radius:12px;padding:12px;margin:8px 0;display:flex;justify-content:space-between;align-items:center;font-weight:600;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:1.5rem;">{rank}</span>
                <span>{name}</span>
                <span style="font-size:0.85rem;color:#6b7c8a;">{badge}</span>
            </div>
            <span style="color:#7eb8d1;">{xp} XP</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
        with col1:
            st.markdown(f"**{rank}**")
        with col2:
            st.markdown(f"**{name}**")
        with col3:
            st.caption(badge)
        with col4:
            st.markdown(f"**{xp} XP**")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Onboarding Checklist ----------
st.markdown("### ✅ Getting Started Checklist")
checklist_items = [
    ("Complete your first mission", prof.get("experiments_completed", 0) > 0),
    ("Set up your profile", bool(prof.get("name") != "Scientist")),
    ("Log data 3 days in a row", prof.get("streak_days", 0) >= 3),
    ("Ask Science Buddy a question", False),  # Could track this
    ("Earn your first badge", len(prof.get("badges", [])) > 0),
]

progress = sum([1 for _, done in checklist_items if done])
st.progress(progress / len(checklist_items))
st.caption(f"{progress}/{len(checklist_items)} completed")

checklist_html = '<div style="margin:16px 0;">'
for task, done in checklist_items:
    icon = "✅" if done else "⬜"
    style = "text-decoration:line-through;color:#aaa;" if done else ""
    checklist_html += f'<div style="padding:8px 0;{style}">{icon} {task}</div>'
checklist_html += '</div>'
st.markdown(checklist_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### 🧭 {t('Missions', LANG)}")
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🌤️ Air & Weather</h4>
            <p style="margin:0 0 24px 0;font-size:0.95rem;">Log temperature, rainfall, and PM2.5. Get an AI mini report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/2_Air_Quality.py", label=t("Open module →", LANG), icon="🌤️")

with c2:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🌱 Seeds & Growth</h4>
            <p style="margin:0 0 24px 0;font-size:0.95rem;">Track plant height and discover growth patterns.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/3_Seeds_Growth.py", label=t("Open module →", LANG), icon="🌱")

with c3:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🐝 Pollinator Patrol</h4>
            <p style="margin:0 0 24px 0;font-size:0.95rem;">Count bees & butterflies to study biodiversity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
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
