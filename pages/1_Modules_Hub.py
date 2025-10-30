import streamlit as st, json, os, pandas as pd, random
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Modules", page_icon="🗂️", layout="wide")
apply_global_theme()

# ---------- CurioLab styles ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');
html, body, [class^="css"], p, li, span, div { 
  font-family: 'Poppins', system-ui, sans-serif; 
  font-weight: 300;
  color: #64748b;
}
h1, h2, h3, h4, .hero h1, .hero h3, .card h3 { 
  font-family: 'Nunito', system-ui, sans-serif; 
  font-weight: 900;
  color: #334155;
}
.card{background:#fff;border-radius:20px;border:2px solid #e2e8f0;padding:20px;box-shadow:0 4px 12px rgba(2,6,23,.06);transition:transform 0.2s ease,box-shadow 0.2s ease}
.card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(2,6,23,.12)}
.card h3{margin:0 0 8px;color:#1e293b}
.theme-box{background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%);border-left:4px solid #0ea5e9;padding:24px;border-radius:12px;margin:24px 0;box-shadow:0 4px 16px rgba(14,165,233,.1)}
.integration-box{background:linear-gradient(135deg,#fef3c7 0%,#fef9e7 100%);border:2px dashed #f59e0b;padding:20px;border-radius:12px;margin:20px 0}
.future-box{background:linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%);border:2px solid #a78bfa;padding:20px;border-radius:12px;margin:20px 0;position:relative;overflow:hidden}
.future-box::before{content:'';position:absolute;top:0;right:0;width:100px;height:100px;background:linear-gradient(135deg,transparent 0%,rgba(167,139,250,0.1) 100%);border-radius:0 0 0 100%}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
header_with_mascot(
    "Modules Hub", 
    "Explore, Compare, Connect", 
    mascot_path="assets/dr_curio.png", 
    size_px=76
)

# ---------- Science Themes Overview ----------
st.markdown("""
<div class='theme-box'>
    <h3 style='margin:0 0 12px 0;color:#0369a1;'>🔬 The Science of Interconnected Systems</h3>
    <p style='margin:0;color:#475569;font-size:1.05rem;line-height:1.7;'>
        Each module explores a layer of environmental systems — <strong>weather</strong>, <strong>growth</strong>, 
        and <strong>biodiversity</strong> — and together, they reveal how life stays in balance. 
        Your observations are chapters in an ongoing study of how Earth's systems interact and sustain each other.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- load existing profile ----------
prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json","r"))
    except Exception:
        prof = {}

# ---------- Module Cards ----------
def count_rows(path):
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

air_rows = count_rows("data/logs_air.csv")
seed_rows = count_rows("data/logs_seeds.csv")
pol_rows = count_rows("data/logs_pollinators.csv")

# Progress Dashboard
st.markdown("### 📊 Your Research Portfolio")
px1, px2, px3, px4 = st.columns(4)
with px1: 
    st.metric("🌤️ Air & Weather", f"{air_rows} observations")
with px2: 
    st.metric("🌱 Seeds & Growth", f"{seed_rows} observations")
with px3: 
    st.metric("🐝 Pollinator Patrol", f"{pol_rows} observations")
with px4: 
    total = air_rows + seed_rows + pol_rows
    st.metric("Total Data Points", f"{total}")

st.markdown("<br>", unsafe_allow_html=True)

# Enhanced Module Cards
st.markdown("### Active Research Modules")
st.caption("Each module is a chapter in your environmental science journey")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class='card' style='border-color:#93c5fd;background:linear-gradient(135deg,#dbeafe 0%,#e0f2fe 100%);'>
      <h3 style='color:#1e40af'>🌤️ Air & Weather</h3>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>What:</strong> Track temperature, rainfall & air quality</p>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>Learn:</strong> Weather patterns & climate science</p>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>Connects to:</strong> How weather affects plant growth and pollinator activity</p>
      <p style='margin:12px 0 0 0;color:#334155'><strong>Observations:</strong> """ + str(air_rows) + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Air_Quality.py", label="Start Module →")

with c2:
    st.markdown("""
    <div class='card' style='border-color:#86efac;background:linear-gradient(135deg,#ecfccb 0%,#f0fdf4 100%);'>
      <h3 style='color:#166534'>🌱 Seeds & Growth</h3>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>What:</strong> Measure plant height & track growth</p>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>Learn:</strong> Photosynthesis & botany</p>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>Connects to:</strong> How temperature and rainfall affect growth rates</p>
      <p style='margin:12px 0 0 0;color:#334155'><strong>Observations:</strong> """ + str(seed_rows) + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Seeds_Growth.py", label="Start Module →")

with c3:
    st.markdown("""
    <div class='card' style='border-color:#fbbf24;background:linear-gradient(135deg,#fef3c7 0%,#fef9e7 100%);'>
      <h3 style='color:#92400e'>🐝 Pollinator Patrol</h3>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>What:</strong> Count bees & butterflies</p>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>Learn:</strong> Biodiversity & ecosystems</p>
      <p style='margin:8px 0;color:#475569;font-size:0.95rem'><strong>Connects to:</strong> How weather patterns influence pollinator behavior</p>
      <p style='margin:12px 0 0 0;color:#334155'><strong>Observations:</strong> """ + str(pol_rows) + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Pollinator_Patrol.py", label="Start Module →")

st.markdown("<br>", unsafe_allow_html=True)

# Integrative Thinking Prompt
if total >= 5:
    st.markdown("""
    <div class='integration-box'>
        <h3 style='margin:0 0 12px 0;color:#92400e;'>🔗 Systems Thinking Challenge</h3>
        <p style='margin:0 0 12px 0;color:#78350f;font-size:1.05rem;'>
            You've collected data across multiple modules! Can you connect what you learned in 
            <strong>Air & Weather</strong> with what's happening in <strong>Seeds & Growth</strong> 
            or <strong>Pollinator Patrol</strong>?
        </p>
        <p style='margin:0;color:#78350f;font-size:0.95rem;font-style:italic;'>
            Think: Does temperature affect plant height? Do bees prefer certain weather conditions? 
            These connections reveal how environmental systems work together.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Integration reflection
    integration_note = st.text_area(
        "Write your observation about how the modules connect:",
        placeholder="Example: I noticed that on warmer days, I see more pollinators, and my plants also grew faster...",
        height=100
    )
    
    if st.button("Save Systems Thinking Note"):
        if integration_note:
            os.makedirs("data", exist_ok=True)
            with open("data/integration_notes.txt", "a") as f:
                f.write(f"\n[{str(pd.Timestamp.now())}] {integration_note}\n")
            st.success("Great observation! This is how scientists think! 🌟")

st.markdown("<br>", unsafe_allow_html=True)

# Mission of the Day
st.markdown("### Today's Recommended Module")
st.caption("Dr. Curio suggests starting here based on your progress")

mission_mods = ["🌤️ Air & Weather", "🌱 Seeds & Growth", "🐝 Pollinator Patrol"]
mission_descs = [
    "Track temperature 3 times today at different times to understand daily patterns",
    "Measure your plant's height and write one observation note about its condition",
    "Spend 10 minutes counting bees or butterflies to understand pollinator diversity"
]

# Suggest module with least observations
counts = [air_rows, seed_rows, pol_rows]
mission_idx = counts.index(min(counts))

st.markdown(f"""
<div style='background:linear-gradient(135deg,#fef9e7 0%,#fffef5 100%);border-left:4px solid #f59e0b;padding:18px;border-radius:12px;'>
    <strong style='color:#92400e;font-size:1.1rem;'>{mission_mods[mission_idx]}</strong>
    <p style='margin:8px 0 0 0;color:#78350f;'>{mission_descs[mission_idx]}</p>
</div>
""", unsafe_allow_html=True)

mission_pages = ["pages/2_Air_Quality.py", "pages/3_Seeds_Growth.py", "pages/4_Pollinator_Patrol.py"]
if st.button(f"Start {mission_mods[mission_idx].split(' ')[1]} Module →", type="primary", use_container_width=True):
    st.switch_page(mission_pages[mission_idx])

st.markdown("<br>", unsafe_allow_html=True)

# Future Modules Teaser
st.markdown("""
<div class='future-box'>
    <h3 style='margin:0 0 12px 0;color:#7c3aed;position:relative;z-index:1;'> Coming Soon: Expanding the Research Lab</h3>
    <p style='margin:0 0 16px 0;color:#6b21a6;font-size:1.05rem;position:relative;z-index:1;'>
        CurioLab is growing! These future modules will deepen your understanding of environmental systems:
    </p>
    <ul style='margin:0;color:#6b21a6;line-height:1.8;position:relative;z-index:1;'>
        <li><strong>🌱 Soil Science</strong> — Analyze pH, moisture, and composition to understand plant health</li>
        <li><strong>🏙️ Urban Ecology</strong> — Study how cities affect wildlife and local ecosystems</li>
        <li><strong>☀️ Light & Energy</strong> — Measure sunlight intensity and its effect on photosynthesis</li>
        <li><strong>💧 Water Quality</strong> — Test local water sources for clarity, temperature, and pH</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Dr. Curio's Science Tips
st.markdown("### Dr. Curio's Research Tips")
tips = [
    "<strong>Consistency is key:</strong> Measure at the same time each day for cleaner data patterns",
    "<strong>Context matters:</strong> Add weather notes to understand what influences your observations",
    "<strong>Control variables:</strong> Try changing just one thing for a week — that's a classic experiment!",
    "<strong>Document everything:</strong> Take photos to create a visual record of your observations",
    "<strong>Look for patterns:</strong> Compare your data week-over-week to discover trends",
    "<strong>Ask 'why?':</strong> When you see something unexpected, that's where discovery begins",
    "<strong>Connect the dots:</strong> Look for relationships between different modules — that's systems thinking"
]
selected_tip = random.choice(tips)

st.markdown(f"""
<div style='background:linear-gradient(135deg,#e0f2fe 0%,#f0f9ff 100%);border-left:4px solid #0ea5e9;padding:18px;border-radius:12px;'>
    <p style='margin:0;color:#0c4a6e;font-size:1rem;'>{selected_tip}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Research Journal Preview
if os.path.exists("data/integration_notes.txt"):
    st.markdown("### Your Journal")
    st.caption("Your notes on how different environmental systems connect")
    
    with open("data/integration_notes.txt", "r") as f:
        notes = f.read()
        if notes.strip():
            st.markdown(f"""
            <div style='background:#f8fafc;border:1px solid #e2e8f0;padding:16px;border-radius:8px;max-height:300px;overflow-y:auto;'>
                <pre style='margin:0;color:#475569;font-size:0.9rem;white-space:pre-wrap;'>{notes}</pre>
            </div>
            """, unsafe_allow_html=True)
