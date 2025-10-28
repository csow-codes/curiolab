import streamlit as st
import json, os, random

# ---------- page config ----------
st.set_page_config(
    page_title="Scientist Homebase",
    page_icon="🧪",
    layout="wide",
)

# ---------- load profile (if any) ----------
prof = {}
if os.path.exists("profile.json"):
    try:
        with open("profile.json", "r") as f:
            prof = json.load(f)
    except Exception:
        prof = {}

# ---------- sidebar: Scientist Homebase + avatar ----------
with st.sidebar:
    st.markdown("### 🏠 Scientist Homebase")   # this shows above the page list
    if prof.get("avatar") and os.path.exists(prof["avatar"]):
        st.image(prof["avatar"], width=120, caption=prof.get("name","Scientist"))
    else:
        st.markdown("*(Create your avatar in **Get Started → Profile**)*")
    st.markdown("---")
    # quick links (works on Streamlit ≥1.39; falls back to markdown)
    try:
        st.page_link("pages/0_Get_Started.py", label="Get Started", icon="🔬")
        st.page_link("pages/1_Modules_Hub.py", label="Modules", icon="🗂️")
        st.page_link("pages/2_Air_Quality.py", label="Air & Weather", icon="🌤️")
        st.page_link("pages/3_Seeds_Growth.py", label="Seeds & Growth", icon="🌱")
    except Exception:
        st.markdown("[🔬 Get Started](pages/0_Get_Started_Profile.py)")
        st.markdown("[🗂️ Modules](pages/1_Modules_Hub.py)")
        st.markdown("[🌤️ Air & Weather](pages/2_Air_Quality.py)")
        st.markdown("[🌱 Seeds & Growth](pages/3_Seeds_Growth.py)")

# ---------- cute UI helper ----------
def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"""
        <div style="
            background:{bg};
            padding:14px 18px;
            border-radius:16px;
            border:1px solid #ede9fe;
            line-height:1.55;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- hero section (pastel gradient) ----------
st.markdown("""
<style>
.hero {
  background: linear-gradient(135deg, #f8f4ff 0%, #fffdfc 100%);
  border-radius: 20px;
  padding: 40px 60px;
  margin-bottom: 28px;
  text-align: center;
  box-shadow: 0 0 10px rgba(167,139,250,0.15);
}
.hero h1 {
  font-size: 2.8rem;
  color: #6b21a8;
  margin: 0 0 8px 0;
}
.hero h3 {
  color: #4c1d95;
  font-weight: 400;
  font-size: 1.25rem;
  margin: 0;
}
</style>
<div class="hero">
  <h1>🧪 LearnLab</h1>
  <h3>Where curiosity meets creativity ✨</h3>
  <p style="color:#555;margin-top:6px;">Turn any classroom or backyard into a mini research lab.</p>
</div>
""", unsafe_allow_html=True)

# welcome message
if prof.get("name"):
    cute_box(f"💫 Welcome back, Dr. {prof['name']}!")
else:
    cute_box("💫 Welcome, scientist! Create your avatar to begin!")

# ---------- get started steps ----------
st.markdown("### 🌱 Get started")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**① Profile**  \nCreate your scientist avatar and pick your interests.")
with c2:
    st.markdown("**② Explore**  \nChoose a module: Air & Weather, Seeds & Growth, Pollinator Patrol.")
with c3:
    st.markdown("**③ Discover**  \nLog data → see charts → get a Mini Science Report 🌟")

go_a, go_b, go_c = st.columns([1,1,1])
with go_a:
    if st.button("✨ Go to Get Started"):
        try:
            st.switch_page("pages/0_Get_Started.py")
        except Exception:
            st.markdown("[Open Get Started → Profile](pages/0_Get_Started.py)")
with go_b:
    if st.button("🗂️ See Modules"):
        try:
            st.switch_page("pages/1_Modules_Hub.py")
        except Exception:
            st.markdown("[Open Modules](pages/1_Modules_Hub.py)")
with go_c:
    if st.button("🌤️ Try Air & Weather"):
        try:
            st.switch_page("pages/2_Air_Quality.py")
        except Exception:
            st.markdown("[Open Air & Weather](pages/2_Air_Quality.py)")

st.markdown("---")

# ---------- featured modules cards ----------
st.markdown("### 🌈 Featured modules")
mc1, mc2, mc3 = st.columns(3)
with mc1:
    st.markdown("#### 🌤️ Air & Weather")
    st.write("Log temperature, rainfall, and PM2.5. See trends and a friendly Mini Science Report.")
    st.markdown("[:arrow_right: Open](pages/2_Air_Quality.py)")
with mc2:
    st.markdown("#### 🌱 Seeds & Growth")
    st.write("Track plant height, compare days, and explore how light & water affect growth.")
    st.markdown("[:arrow_right: Open](pages/3_Seeds_Growth.py)")
with mc3:
    st.markdown("#### 🐝 Pollinator Patrol")
    st.write("Count bees & butterflies to study biodiversity in your neighborhood.")
    try:
        st.markdown("[:arrow_right: Open](pages/4_Pollinator_Patrol.py)")
    except Exception:
        st.write("_Add this page later if you like!_")

st.markdown("---")

# ---------- why it matters / footer ----------
st.subheader("💬 Why it matters")
st.write(
    "LearnLab makes **STEM accessible** anywhere. It blends simple data collection with clear visuals "
    "and optional AI summaries—so every kid can feel like a real scientist."
)

st.caption("Built by Charlize S., another fellow scientist ❤️")
st.balloons()
