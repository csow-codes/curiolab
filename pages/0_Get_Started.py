import streamlit as st, json, os, random, base64
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Get Started", page_icon="🔬", layout="wide")

# Global zoom effect - scale everything down to 75%
st.markdown("""
<style>
/* Scale down all content */
.main .block-container {
    zoom: 0.75;
    -moz-transform: scale(0.75);
    -moz-transform-origin: 0 0;
}
/* Adjust max-width to accommodate zoom */
.main .block-container {
    max-width: 1400px;
}
</style>
""", unsafe_allow_html=True)

apply_global_theme()

# Header
header_with_mascot("CurioLab", "Get Started: Create your scientist profile and begin exploring!", mascot_path="assets/dr_curio.png", size_px=140)

# Super cute styling
st.markdown("""
<style>
.hero { padding: 40px 50px; }
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

st.markdown("### Step 1 — Create Your Scientist Profile")
cute_box("Your profile saves locally. Pick a name, interests, and language.", bg="#e0f2fe")

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
    st.markdown("#### About You")
    bio = st.text_area("What makes you curious? (Optional)", placeholder="E.g., I love watching plants grow or learning about weather!", height=80, value=prof.get("bio", ""))

    st.markdown("---")
    st.markdown("#### Starter Badges Preview")
    b1,b2,b3 = st.columns(3)
    with b1: st.markdown("<div style='background:#ecfccb;padding:12px;border-radius:12px;border:1px solid #a3e635;text-align:center'>Seedling Scientist</div>", unsafe_allow_html=True)
    with b2: st.markdown("<div style='background:#e0f2fe;padding:12px;border-radius:12px;border:1px solid #93c5fd;text-align:center'>Weather Watcher</div>", unsafe_allow_html=True)
    with b3: st.markdown("<div style='background:#fef3c7;padding:12px;border-radius:12px;border:1px solid #fbbf24;text-align:center'>Pollinator Pal</div>", unsafe_allow_html=True)

    # Save profile button
    if st.button("Save My Profile", type="primary", use_container_width=True):
        avatar_emoji = generate_scientist_emoji(name)
        prof_new = {
            "name": name, "age": age, "topics": topics, "language": language,
            "avatar": avatar_emoji,  # Store emoji instead of image path
            "bio": bio,
            "xp": prof.get("xp", 0), "streak_days": prof.get("streak_days", 0),
            "last_log_date": prof.get("last_log_date", None)
        }
        json.dump(prof_new, open("profile.json","w"))
        st.success(f"Welcome to CurioLab, {name}! Your profile is saved.")
        st.balloons()

with right:
    st.markdown("### Step 2 — How CurioLab Works")
    cute_box("1) Observe → 2) Log data → 3) See charts → 4) Get a Mini Science Report → 5) Share a Science Card", bg="#ecfccb")
    st.markdown("#### Dr. Curio's Tip")
    tips = [
        "Measure at the same time each day for smoother trends!",
        "Add notes about weather or sunlight—context makes your science stronger!",
        "Try a mini experiment: change one thing and watch the effect!",
    ]
    st.info(random.choice(tips))

    st.markdown("### Step 3 — Jump In")
    c1,c2,c3 = st.columns(3)
    with c1: st.page_link("pages/2_Air_Quality.py", label="Start: Air & Weather")
    with c2: st.page_link("pages/3_Seeds_Growth.py", label="Start: Seeds & Growth")
    with c3: st.page_link("pages/4_Pollinator_Patrol.py", label="Start: Pollinator Patrol")
