import streamlit as st, json, os, random, base64
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Get Started", page_icon="🔬", layout="wide")
apply_global_theme()
header_with_mascot("Welcome to CurioLab", "Meet Dr. Curio and set up your profile.")

def cute_box(text: str, bg="#e0f2fe"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

# --- CurioLab hero styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');
html, body, [class^="css"], p, li, span, div { 
  font-family: 'Poppins', system-ui, sans-serif; 
  font-weight: 300;
  color: #a4a4a4;
}
h1, h2, h3, h4, .hero h1, .hero h3 { 
  font-family: 'Nunito', system-ui, sans-serif; 
  font-weight: 900;
  color: #7c9aa8;
}
.hero{background:linear-gradient(135deg,#e0f2fe 0%,#f0f9ff 60%,#ecfccb 100%);border-radius:28px;padding:42px 54px;margin-bottom:28px;text-align:center;box-shadow:0 8px 24px rgba(59,130,246,.18);border:2px solid #bfdbfe}
.hero h1{font-size:2.6rem;margin:0 0 8px}
.hero p{color:#a4a4a4;margin:6px 0 0 0;font-weight:300}
.logo-curio{animation:bounce 2s ease-in-out infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
</style>
""", unsafe_allow_html=True)

def generate_scientist_emoji(name):
    """Generate a unique emoji for each scientist based on their name"""
    emojis = ["🧪", "🔬", "🌱", "🌤️", "🐝", "🔭", "⚗️", "🌍", "🧬", "🔍"]
    random.seed(name)
    return random.choice(emojis)

prof = {}
if os.path.exists("profile.json"):
    try: prof = json.load(open("profile.json","r"))
    except Exception: prof = {}

st.markdown("### 📝 Step 1 — Create Your Scientist Profile")
cute_box("Your profile saves locally. Pick a name, interests, and language. ✨", bg="#e0f2fe")

left, right = st.columns([1,1.2], gap="large")

with left:
    name = st.text_input("Your name or nickname", value=prof.get("name", "Alex"), help="Shown on your CurioLab cards")

    # --- Safe age selectbox ---
    AGE_CHOICES = ["8–10", "11–13", "14–16"]
    saved_age = prof.get("age")
    if saved_age not in AGE_CHOICES:
        age_index = 1  # default to "11–13"
    else:
        age_index = AGE_CHOICES.index(saved_age)
    age = st.selectbox("Age range", AGE_CHOICES, index=age_index)

    # --- Topics ---
    topics = st.multiselect(
        "Favorite topics",
        ["Environment", "Plants", "Weather", "Health", "Physics", "Space"],
        default=prof.get("topics", ["Environment"])
    )

    # --- Safe language selectbox ---
    LANG_CHOICES = ["English", "Español", "简体中文"]
    saved_lang = prof.get("language", "English")
    lang_index = LANG_CHOICES.index(saved_lang) if saved_lang in LANG_CHOICES else 0
    language = st.selectbox("Language", LANG_CHOICES, index=lang_index)

    st.markdown("---")
    st.markdown("#### 💭 About You")
    bio = st.text_area("What makes you curious? (Optional)", placeholder="E.g., I love watching plants grow or learning about weather! 🌱", height=80, value=prof.get("bio", ""))

    st.markdown("---")
    st.markdown("#### 🎖️ Starter Badges Preview")
    b1,b2,b3 = st.columns(3)
    with b1: st.markdown("<div style='background:#ecfccb;padding:12px;border-radius:12px;border:1px solid #a3e635;text-align:center'>🌱 Seedling Scientist</div>", unsafe_allow_html=True)
    with b2: st.markdown("<div style='background:#e0f2fe;padding:12px;border-radius:12px;border:1px solid #93c5fd;text-align:center'>🌤️ Weather Watcher</div>", unsafe_allow_html=True)
    with b3: st.markdown("<div style='background:#fef3c7;padding:12px;border-radius:12px;border:1px solid #fbbf24;text-align:center'>🐝 Pollinator Pal</div>", unsafe_allow_html=True)

    # Save profile button
    if st.button("✨ Save My Profile", type="primary", use_container_width=True):
        avatar_emoji = generate_scientist_emoji(name)
        prof_new = {
            "name": name, "age": age, "topics": topics, "language": language,
            "avatar": avatar_emoji,  # Store emoji instead of image path
            "bio": bio,
            "xp": prof.get("xp", 0), "streak_days": prof.get("streak_days", 0),
            "last_log_date": prof.get("last_log_date", None)
        }
        json.dump(prof_new, open("profile.json","w"))
        st.success(f"Welcome to CurioLab, {name}! 🎉 Your profile is saved.")
        st.balloons()

with right:
    st.markdown("### 🧪 Step 2 — How CurioLab Works")
    cute_box("1) Observe → 2) Log data → 3) See charts → 4) Get a Mini Science Report → 5) Share a Science Card", bg="#ecfccb")
    st.markdown("#### 💬 Dr. Curio's Tip")
    tips = [
        "Measure at the same time each day for smoother trends!",
        "Add notes about weather or sunlight—context makes your science stronger!",
        "Try a mini experiment: change one thing and watch the effect!",
    ]
    st.info(random.choice(tips))

    st.markdown("### 🚀 Step 3 — Jump In")
    c1,c2,c3 = st.columns(3)
    with c1: st.page_link("pages/2_Air_Quality.py", label="Start: Air & Weather", icon="🌤️")
    with c2: st.page_link("pages/3_Seeds_Growth.py", label="Start: Seeds & Growth", icon="🌱")
    with c3: st.page_link("pages/4_Pollinator_Patrol.py", label="Start: Pollinator Patrol", icon="🐝")
