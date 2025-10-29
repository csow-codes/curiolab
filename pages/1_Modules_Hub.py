import streamlit as st, json, os, base64, pandas as pd, random

st.set_page_config(page_title="Modules", page_icon="🗂️", layout="wide")

# ---------- cute helpers ----------
def cute_box(text: str, bg="#e0f2fe"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #bfdbfe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

# ---------- CurioLab styles ----------
st.markdown("""
<style>
.hero{background:linear-gradient(135deg,#e0f2fe 0%,#f0f9ff 60%,#ecfccb 100%);border-radius:28px;padding:42px 54px;margin-bottom:28px;text-align:center;box-shadow:0 8px 24px rgba(59,130,246,.18);border:2px solid #bfdbfe}
.hero h1{font-size:2.6rem;color:#1e40af;margin:0 0 8px;font-weight:800}
.hero p{color:#475569;margin:6px 0 0 0}
.logo-curio{animation:bounce 2s ease-in-out infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.card{background:#fff;border-radius:20px;border:2px solid #e2e8f0;padding:20px;box-shadow:0 4px 12px rgba(2,6,23,.06)}
.card h3{margin:0 0 8px}
</style>
""", unsafe_allow_html=True)

# ---------- load existing profile ----------
prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json","r"))
    except Exception:
        prof = {}

# ---------- Hero ----------
logo_path = "avatars/curio_logo.png"
if os.path.exists(logo_path):
    _b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(f"""
    <div class='hero'>
      <div style='display:flex;align-items:center;justify-content:center;gap:16px;'>
        <img class='logo-curio' src='data:image/png;base64,{_b64}' style='width:70px;height:70px;border-radius:14px;'>
        <h1>CurioLab Modules</h1>
        <span style='font-size:2rem'>🗂️</span>
      </div>
      <p>Explore hands-on science missions guided by <strong>Dr. Curio</strong> the capybara.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='hero'>
      <div style='display:flex;align-items:center;justify-content:center;gap:16px;'>
        <span class='logo-curio' style='font-size:2.6rem'>🦫</span>
        <h1>CurioLab Modules</h1>
        <span style='font-size:2rem'>🗂️</span>
      </div>
      <p>Explore hands-on science missions guided by <strong>Dr. Curio</strong> the capybara.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Module Cards ----------
def count_rows(path):
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

air_rows = count_rows("data/logs_air.csv")
seed_rows = count_rows("data/logs_seeds.csv")
pol_rows = count_rows("data/logs_pollinators.csv")

# Progress Dashboard
st.markdown("### 📊 Your Science Progress")
px1, px2, px3, px4 = st.columns(4)
with px1: 
    st.metric("🌤️ Air & Weather", f"{air_rows} observations")
with px2: 
    st.metric("🌱 Seeds & Growth", f"{seed_rows} observations")
with px3: 
    st.metric("🐝 Pollinator Patrol", f"{pol_rows} observations")
with px4: 
    total = air_rows + seed_rows + pol_rows
    st.metric("📊 Total Data Points", f"{total}")

# Mission of the Day
st.markdown("---")
st.markdown("### ⭐ Dr. Curio's Mission of the Day")
mission_mods = ["🌤️ Air & Weather", "🌱 Seeds & Growth", "🐝 Pollinator Patrol"]
mission_descs = [
    "Track temperature 3 times today at different times! 🌡️",
    "Measure your plant's height and write one observation note! 🌱",
    "Spend 10 minutes counting bees or butterflies in your yard! 🐝"
]
random.seed(1)
mission_idx = random.randint(0, 2)
cute_box(f"{mission_mods[mission_idx]}: {mission_descs[mission_idx]}", bg="#fef3c7", emoji="✨")
# Mission button routing
mission_pages = ["pages/2_Air_Quality.py", "pages/3_Seeds_Growth.py", "pages/4_Pollinator_Patrol.py"]
if st.button(f"Start {mission_mods[mission_idx].split(' ')[1]} Mission →", type="primary", use_container_width=True):
    st.switch_page(mission_pages[mission_idx])

st.markdown("---")

# Enhanced Module Cards
st.markdown("### 🧪 Choose Your Mission")

c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class='card' style='border-color:#93c5fd;background:linear-gradient(135deg,#dbeafe 0%,#e0f2fe 100%);'>
      <h3 style='color:#1e40af'>🌤️ Air & Weather</h3>
      <p style='margin:8px 0;color:#475569'><strong>What:</strong> Track temperature, rainfall & air quality</p>
      <p style='margin:8px 0;color:#475569'><strong>Learn:</strong> Weather patterns & climate science</p>
      <p style='margin:8px 0;color:#334155'><strong>Observations:</strong> """ + str(air_rows) + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Air_Quality.py", label="Start Mission →", icon="🌤️")
with c2:
    st.markdown("""
    <div class='card' style='border-color:#86efac;background:linear-gradient(135deg,#ecfccb 0%,#f0fdf4 100%);'>
      <h3 style='color:#166534'>🌱 Seeds & Growth</h3>
      <p style='margin:8px 0;color:#475569'><strong>What:</strong> Measure plant height & track growth</p>
      <p style='margin:8px 0;color:#475569'><strong>Learn:</strong> Photosynthesis & botany</p>
      <p style='margin:8px 0;color:#334155'><strong>Observations:</strong> """ + str(seed_rows) + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Seeds_Growth.py", label="Start Mission →", icon="🌱")
with c3:
    st.markdown("""
    <div class='card' style='border-color:#fbbf24;background:linear-gradient(135deg,#fef3c7 0%,#fef9e7 100%);'>
      <h3 style='color:#92400e'>🐝 Pollinator Patrol</h3>
      <p style='margin:8px 0;color:#475569'><strong>What:</strong> Count bees & butterflies</p>
      <p style='margin:8px 0;color:#475569'><strong>Learn:</strong> Biodiversity & ecosystems</p>
      <p style='margin:8px 0;color:#334155'><strong>Observations:</strong> """ + str(pol_rows) + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Pollinator_Patrol.py", label="Start Mission →", icon="🐝")

st.markdown("---")
st.markdown("### 💡 Dr. Curio's Science Tips")
tips = [
    "💡 Measure at the same time each day for smoother trends!",
    "💡 Add weather notes—context powers your conclusions!",
    "💡 Try changing just one thing for a week—classic experiment!",
    "💡 Take photos to document your observations!",
    "💡 Compare your data week-over-week to find patterns!"
]
selected_tip = random.choice(tips)
cute_box(selected_tip, bg="#e0f2fe", emoji="🦫")