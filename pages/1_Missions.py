import streamlit as st, os, json, pandas as pd, datetime as dt
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Missions", page_icon="🔬", layout="wide")
apply_global_theme()

# Custom CSS
st.markdown("""
<style>
.hero{background:linear-gradient(135deg,#e8f3f8 0%,#f6fbff 60%,#ffffff 100%);border-radius:24px;padding:36px 44px;margin-bottom:20px;text-align:center;box-shadow:0 8px 24px rgba(124,154,168,.18);border:1px solid #dce9f0}
.card{background:#f6f9fb;border-radius:16px;border:1px solid #e2e8f0;padding:20px;box-shadow:0 4px 12px rgba(2,6,23,.04);transition:transform 0.2s ease,box-shadow 0.2s ease}
.card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(2,6,23,.12)}
.card h3{margin:0 0 8px}
.philosophy-box{background:linear-gradient(135deg,#fef9e7 0%,#fffef5 100%);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin:24px 0;box-shadow:0 4px 16px rgba(245,158,11,.1)}
.hypothesis-box{background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%);border:2px dashed #3b82f6;padding:18px;border-radius:12px;margin:16px 0}
.reflection-box{background:linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%);border:2px solid #8b5cf6;padding:18px;border-radius:12px;margin:16px 0}
.stat-badge{display:inline-block;background:#10b981;color:white;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:600;margin-left:8px}
</style>
""", unsafe_allow_html=True)

def count_rows(path): 
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

# Header
header_with_mascot(
    "CurioLab Missions", 
    "From Observation to Understanding", 
    mascot_path="assets/dr_curio.png", 
    size_px=76
)

# Mission Philosophy
st.markdown("""
<div class='philosophy-box'>
    <h3 style='margin:0 0 12px 0;color:#92400e;'>🔬 Mission Philosophy</h3>
    <p style='margin:0;color:#78350f;font-size:1.05rem;line-height:1.6;'>
        Each mission begins with a question and ends with a discovery. Your goal isn't to finish — 
        it's to <strong>notice more deeply</strong>. Real science happens when you stay curious, 
        ask "why?", and let your observations surprise you.
    </p>
</div>
""", unsafe_allow_html=True)

# Progress Dashboard
prof = {}
if os.path.exists("profile.json"):
    try: 
        prof = json.load(open("profile.json","r"))
    except Exception: 
        prof = {}
prof.setdefault("xp", 0)
prof.setdefault("streak_days", 0)
prof.setdefault("experiments_completed", 0)

st.markdown("### 📊 Your Research Studio")
px1, px2, px3 = st.columns(3)
with px1: 
    st.metric("XP", f"{prof['xp']%100}/100", delta="+5 per observation")
with px2: 
    st.metric("Streak", f"{prof['streak_days']} days", delta="🔥" if prof['streak_days'] > 0 else None)
with px3: 
    st.metric("Total Experiments", prof['experiments_completed'])

st.markdown("<br>", unsafe_allow_html=True)

# Hypothesis tracking
if 'hypotheses' not in st.session_state:
    st.session_state.hypotheses = {}
if 'reflections' not in st.session_state:
    st.session_state.reflections = {}

# Load saved hypotheses and reflections
if os.path.exists("data/hypotheses.json"):
    try:
        st.session_state.hypotheses = json.load(open("data/hypotheses.json", "r"))
    except:
        pass

if os.path.exists("data/reflections.json"):
    try:
        st.session_state.reflections = json.load(open("data/reflections.json", "r"))
    except:
        pass

# Count observations
air_rows = count_rows("data/logs_air.csv")
seed_rows = count_rows("data/logs_seeds.csv")
pol_rows = count_rows("data/logs_pollinators.csv")

st.markdown("### 🎯 Active Missions")

c1, c2, c3 = st.columns(3)

# Mission 1: Air & Weather
with c1:
    st.markdown("""
    <div class='card' style='border-color:#93c5fd;background:linear-gradient(135deg,#dbeafe 0%,#e0f2fe 100%);'>
      <h3 style='color:#1e40af'>🌤️ Air & Weather</h3>
      <p style='margin:0 0 12px 0;color:#334155;font-size:0.95rem;'>Track temperature, rainfall, and air quality patterns in your environment.</p>
      <p style='margin:0;color:#334155'>Observations: <strong>""" + str(air_rows) + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hypothesis for Air & Weather
    if air_rows == 0:
        st.markdown("""
        <div class='hypothesis-box'>
            <strong style='color:#1e40af'>💭 Before you start...</strong>
            <p style='margin:8px 0 0 0;font-size:0.9rem;color:#475569'>What do you think you'll discover about weather patterns?</p>
        </div>
        """, unsafe_allow_html=True)
        
        hyp = st.text_area("Your hypothesis:", key="hyp_air", placeholder="I think temperature will...", height=80)
        if st.button("Save Hypothesis", key="save_hyp_air"):
            st.session_state.hypotheses['air'] = {"text": hyp, "date": str(dt.date.today())}
            os.makedirs("data", exist_ok=True)
            json.dump(st.session_state.hypotheses, open("data/hypotheses.json", "w"))
            st.success("Hypothesis saved! 🎯")
    else:
        # Show saved hypothesis
        if 'air' in st.session_state.hypotheses:
            st.markdown(f"""
            <div class='hypothesis-box'>
                <strong style='color:#1e40af'>💭 Your hypothesis:</strong>
                <p style='margin:8px 0 0 0;font-size:0.9rem;color:#475569;font-style:italic'>"{st.session_state.hypotheses['air']['text']}"</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.page_link("pages/2_Air_Quality.py", label="Start Mission →")
    
    # Reflection after observations
    if air_rows >= 3 and 'air' not in st.session_state.reflections:
        st.markdown("""
        <div class='reflection-box'>
            <strong style='color:#7c3aed'>✨ Reflection Time</strong>
            <p style='margin:8px 0 0 0;font-size:0.9rem;color:#5b21b6'>You've made some observations! What surprised you most?</p>
        </div>
        """, unsafe_allow_html=True)
        
        ref = st.text_area("Your reflection:", key="ref_air", placeholder="I was surprised that...", height=80)
        if st.button("Save Reflection", key="save_ref_air"):
            st.session_state.reflections['air'] = {"text": ref, "date": str(dt.date.today())}
            os.makedirs("data", exist_ok=True)
            json.dump(st.session_state.reflections, open("data/reflections.json", "w"))
            st.success("Reflection saved! ✨")

# Mission 2: Seeds & Growth
with c2:
    st.markdown("""
    <div class='card' style='border-color:#86efac;background:linear-gradient(135deg,#ecfccb 0%,#f0fdf4 100%);'>
      <h3 style='color:#166534'>🌱 Seeds & Growth</h3>
      <p style='margin:0 0 12px 0;color:#334155;font-size:0.95rem;'>Measure plant growth and discover the factors that help life flourish.</p>
      <p style='margin:0;color:#334155'>Observations: <strong>""" + str(seed_rows) + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hypothesis for Seeds
    if seed_rows == 0:
        st.markdown("""
        <div class='hypothesis-box'>
            <strong style='color:#1e40af'>💭 Before you start...</strong>
            <p style='margin:8px 0 0 0;font-size:0.9rem;color:#475569'>What factors do you think affect plant growth most?</p>
        </div>
        """, unsafe_allow_html=True)
        
        hyp = st.text_area("Your hypothesis:", key="hyp_seed", placeholder="I predict plants will grow faster when...", height=80)
        if st.button("Save Hypothesis", key="save_hyp_seed"):
            st.session_state.hypotheses['seed'] = {"text": hyp, "date": str(dt.date.today())}
            os.makedirs("data", exist_ok=True)
            json.dump(st.session_state.hypotheses, open("data/hypotheses.json", "w"))
            st.success("Hypothesis saved! 🎯")
    else:
        if 'seed' in st.session_state.hypotheses:
            st.markdown(f"""
            <div class='hypothesis-box'>
                <strong style='color:#1e40af'>💭 Your hypothesis:</strong>
                <p style='margin:8px 0 0 0;font-size:0.9rem;color:#475569;font-style:italic'>"{st.session_state.hypotheses['seed']['text']}"</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.page_link("pages/3_Seeds_Growth.py", label="Start Mission →")
    
    if seed_rows >= 3 and 'seed' not in st.session_state.reflections:
        st.markdown("""
        <div class='reflection-box'>
            <strong style='color:#7c3aed'>✨ Reflection Time</strong>
            <p style='margin:8px 0 0 0;font-size:0.9rem;color:#5b21b6'>What patterns did you notice in plant growth?</p>
        </div>
        """, unsafe_allow_html=True)
        
        ref = st.text_area("Your reflection:", key="ref_seed", placeholder="The most interesting pattern was...", height=80)
        if st.button("Save Reflection", key="save_ref_seed"):
            st.session_state.reflections['seed'] = {"text": ref, "date": str(dt.date.today())}
            os.makedirs("data", exist_ok=True)
            json.dump(st.session_state.reflections, open("data/reflections.json", "w"))
            st.success("Reflection saved! ✨")

# Mission 3: Pollinator Patrol
with c3:
    st.markdown("""
    <div class='card' style='border-color:#fbbf24;background:linear-gradient(135deg,#fef3c7 0%,#fef9e7 100%);'>
      <h3 style='color:#92400e'>🐝 Pollinator Patrol</h3>
      <p style='margin:0 0 12px 0;color:#334155;font-size:0.95rem;'>Count bees and butterflies to understand biodiversity in your area.</p>
      <p style='margin:0;color:#334155'>Observations: <strong>""" + str(pol_rows) + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hypothesis for Pollinators
    if pol_rows == 0:
        st.markdown("""
        <div class='hypothesis-box'>
            <strong style='color:#1e40af'>💭 Before you start...</strong>
            <p style='margin:8px 0 0 0;font-size:0.9rem;color:#475569'>Which pollinators do you expect to see most often?</p>
        </div>
        """, unsafe_allow_html=True)
        
        hyp = st.text_area("Your hypothesis:", key="hyp_pol", placeholder="I think I'll see more bees than butterflies because...", height=80)
        if st.button("Save Hypothesis", key="save_hyp_pol"):
            st.session_state.hypotheses['pollinator'] = {"text": hyp, "date": str(dt.date.today())}
            os.makedirs("data", exist_ok=True)
            json.dump(st.session_state.hypotheses, open("data/hypotheses.json", "w"))
            st.success("Hypothesis saved! 🎯")
    else:
        if 'pollinator' in st.session_state.hypotheses:
            st.markdown(f"""
            <div class='hypothesis-box'>
                <strong style='color:#1e40af'>💭 Your hypothesis:</strong>
                <p style='margin:8px 0 0 0;font-size:0.9rem;color:#475569;font-style:italic;">"{st.session_state.hypotheses['pollinator']['text']}"</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.page_link("pages/4_Pollinator_Patrol.py", label="Start Mission →")
    
    if pol_rows >= 3 and 'pollinator' not in st.session_state.reflections:
        st.markdown("""
        <div class='reflection-box'>
            <strong style='color:#7c3aed'>✨ Reflection Time</strong>
            <p style='margin:8px 0 0 0;font-size:0.9rem;color:#5b21b6'>What surprised you about pollinator behavior?</p>
        </div>
        """, unsafe_allow_html=True)
        
        ref = st.text_area("Your reflection:", key="ref_pol", placeholder="I noticed that...", height=80)
        if st.button("Save Reflection", key="save_ref_pol"):
            st.session_state.reflections['pollinator'] = {"text": ref, "date": str(dt.date.today())}
            os.makedirs("data", exist_ok=True)
            json.dump(st.session_state.reflections, open("data/reflections.json", "w"))
            st.success("Reflection saved! ✨")

st.markdown("<br><br>", unsafe_allow_html=True)

# Show all reflections if any exist
if st.session_state.reflections:
    st.markdown("### 📝 Your Research Journal")
    st.caption("Your scientific reflections and discoveries")
    
    for mission, data in st.session_state.reflections.items():
        mission_emoji = {"air": "🌤️", "seed": "🌱", "pollinator": "🐝"}.get(mission, "🔬")
        mission_name = {"air": "Air & Weather", "seed": "Seeds & Growth", "pollinator": "Pollinator Patrol"}.get(mission, mission)
        
        st.markdown(f"""
        <div style='background:#f8fafc;border-left:4px solid #3b82f6;padding:16px;border-radius:8px;margin:12px 0;'>
            <strong style='color:#1e40af'>{mission_emoji} {mission_name}</strong>
            <p style='margin:8px 0 4px 0;color:#475569;font-style:italic;'>"{data['text']}"</p>
            <small style='color:#94a3b8;'>Reflected on {data['date']}</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Teacher & Coach Section
st.subheader("🎓 Teacher & Coach")
colA, colB = st.columns(2)

with colA:
    st.write("**Download CSV logs:**")
    if os.path.exists("data/logs_air.csv"): 
        st.download_button("⬇️ Air & Weather CSV", data=open("data/logs_air.csv","rb").read(), file_name="logs_air.csv")
    if os.path.exists("data/logs_seeds.csv"): 
        st.download_button("⬇️ Seeds & Growth CSV", data=open("data/logs_seeds.csv","rb").read(), file_name="logs_seeds.csv")
    if os.path.exists("data/logs_pollinators.csv"): 
        st.download_button("⬇️ Pollinators CSV", data=open("data/logs_pollinators.csv","rb").read(), file_name="logs_pollinators.csv")
    
    # Download hypotheses and reflections
    if st.session_state.hypotheses:
        hyp_json = json.dumps(st.session_state.hypotheses, indent=2)
        st.download_button("⬇️ Student Hypotheses (JSON)", data=hyp_json, file_name="hypotheses.json")
    if st.session_state.reflections:
        ref_json = json.dumps(st.session_state.reflections, indent=2)
        st.download_button("⬇️ Student Reflections (JSON)", data=ref_json, file_name="reflections.json")

with colB:
    st.write("**Quick feedback (1–2 questions)**")
    ease = st.slider("How easy was CurioLab to use?", 1, 5, 4)
    conf = st.slider("Do the charts make sense?", 1, 5, 4)
    msg = st.text_input("One thing to improve", "")
    
    if st.button("Submit feedback"):
        os.makedirs("data", exist_ok=True)
        with open("data/feedback.csv", "a") as f:
            f.write(f"{str(dt.date.today())},{ease},{conf},{msg}\n")
        st.success("Thanks! ✨")
    
    if os.path.exists("data/feedback.csv"):
        try:
            fb = pd.read_csv("data/feedback.csv", header=None, names=["date","ease","conf","msg"])
            st.caption(f"Feedback so far — ease: {fb['ease'].mean():.1f}/5, understanding: {fb['conf'].mean():.1f}/5 (n={len(fb)})")
        except:
            pass
