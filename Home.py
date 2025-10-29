import streamlit as st, json, os, random, datetime as dt, base64
from lang import t

st.set_page_config(page_title="CurioLab - Home", page_icon="🧪", layout="wide")

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

# ---------- CSS: animated hero + cute UI with CurioLab branding ----------
st.markdown("""
<style>
.hero{background:linear-gradient(135deg,#e0f2fe 0%,#f0f9ff 50%,#fff7ed 100%);border-radius:28px;padding:50px 60px;margin-bottom:32px;text-align:center;box-shadow:0 8px 24px rgba(59,130,246,.2);border:2px solid #bfdbfe}
.hero h1{font-size:3.5rem;color:#1e40af;margin:0 0 12px;text-shadow:2px 2px 8px rgba(59,130,246,.2);font-weight:bold}
.hero h3{color:#3b82f6;font-weight:500;font-size:1.4rem;margin:4px 0}
.hero p{color:#64748b;font-size:1.1rem;margin:8px 0 0 0}
.logo-bear{animation:bounce 2s ease-in-out infinite}
@keyframes bounce{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-10px) scale(1.05)}}
.floaty{animation:float 4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.card:hover{transform:scale(1.02);transition:all 0.3s ease}
.curio-badge{background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%);color:white;padding:8px 20px;border-radius:20px;display:inline-block;margin:12px auto;font-size:0.9rem;box-shadow:0 4px 12px rgba(59,130,246,.3);font-weight:600}
</style>
""", unsafe_allow_html=True)

# ---------- sidebar avatar / XP ----------
with st.sidebar:
    st.markdown("### CurioLab")
    if prof.get("avatar") and os.path.exists(prof["avatar"]):
        st.image(prof["avatar"], width=120, caption=prof.get("name","Scientist"))
    st.markdown("#### 📊 Your Progress")
    st.progress(min(prof["xp"] % 100, 100))
    st.caption(f"✨ XP: {prof['xp']%100}/100")
    st.caption(f"🔥 Streak: {prof['streak_days']} days")
    st.markdown("---")
    st.markdown("### 🔎 Quick links")
    try:
        st.page_link("pages/0_Get_Started.py", label="Get Started", icon="")
        st.page_link("pages/1_Missions.py", label="🧭 Missions", icon="")
        st.page_link("pages/2_Air_Quality.py", label="🌤️ Air & Weather", icon="")
        st.page_link("pages/3_Seeds_Growth.py", label="🌱 Seeds & Growth", icon="")
        st.page_link("pages/4_Pollinator_Patrol.py", label="🐝 Pollinator Patrol", icon="")
        st.page_link("pages/5_Analysis_Lab.py", label="📊 Analysis Lab", icon="")
    except Exception as e:
        st.write("Pages will appear after you add them.")

# ---------- Hero with CurioLab Branding ----------
# Check if custom logo exists, otherwise use emoji
logo_path = "avatars/curio_logo.png"
if os.path.exists(logo_path):
    _logo_b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(f"""
    <div class="hero">
      <div style="display:flex;align-items:center;justify-content:center;gap:20px;margin-bottom:20px;">
        <img class="logo-curio" src="data:image/png;base64,{_logo_b64}" style="width:80px;height:80px;">
        <h1>CurioLab</h1>
        <span class="logo-curio" style="font-size:4rem;">🔬</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero">
      <div style="display:flex;align-items:center;justify-content:center;gap:20px;margin-bottom:20px;">
        <span class="logo-curio" style="font-size:5rem;">💫</span>
        <h1>CurioLab</h1>
        <span class="logo-curio" style="font-size:4rem;">🔬</span>
      </div>
      <h3>Where curious minds discover science ✨</h3>
      <p>Join Dr. Curio in turning any classroom or backyard into your own research lab!</p>
      <div class="curio-badge">@CURIOLAB</div>
      <div style="display:flex;justify-content:center;gap:20px;margin-top:20px;">
        <span class="floaty" style="font-size:2.5rem;">🧪</span>
        <span class="floaty" style="font-size:2.5rem;">🌱</span>
        <span class="floaty" style="font-size:2.5rem;">🌤️</span>
        <span class="floaty" style="font-size:2.5rem;">🐝</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- Daily challenge ----------
daily_options = [
    "Measure temperature 3 times today 🌡️",
    "Observe cloud types for 10 minutes ☁️",
    "Sketch 3 leaves you find 🍃",
    "Count bees or butterflies for 10 minutes 🐝🦋",
    "Track plant height for your growth experiment 🌱",
    "Record air quality at different times of day 💨",
]
random.seed(dt.date.today().toordinal())
daily = random.choice(daily_options)
st.markdown(f"""
<div style='background:linear-gradient(135deg,#dbeafe 0%,#e0f2fe 100%);padding:20px;border-radius:16px;border-left:4px solid #3b82f6;margin:20px 0;'>
  <h3 style='color:#1e40af;margin:0 0 8px;'>🌞 Daily Challenge</h3>
  <p style='color:#334155;margin:0;font-size:1.1rem;'>{daily}</p>
</div>
""", unsafe_allow_html=True)

# ---------- Missions (cards) with Curio Lab blue theme ----------
st.markdown(f"### 🧭 Science Missions")
st.markdown("<p style='color:#64748b;margin-bottom:16px;'>Choose a module to start your scientific adventure!</p>", unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#dbeafe 0%,#e0f2fe 100%);padding:24px;border-radius:20px;border:2px solid #93c5fd;box-shadow:0 4px 12px rgba(59,130,246,.15);'>
      <h3 style='color:#1e40af;margin:0 0 12px;'>🌤️ Air & Weather</h3>
      <p style='color:#475569;margin:0;'>Track temperature, rainfall, and air quality. Analyze weather patterns!</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Air_Quality.py", label="Start Mission →", icon="🌤️")
with c2:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#ecfccb 0%,#f0fdf4 100%);padding:24px;border-radius:20px;border:2px solid #86efac;box-shadow:0 4px 12px rgba(34,197,94,.15);'>
      <h3 style='color:#166534;margin:0 0 12px;'>🌱 Seeds & Growth</h3>
      <p style='color:#475569;margin:0;'>Measure plant height, discover growth patterns, and conduct experiments!</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Seeds_Growth.py", label="Start Mission →", icon="🌱")
with c3:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#fef3c7 0%,#fef9e7 100%);padding:24px;border-radius:20px;border:2px solid #fbbf24;box-shadow:0 4px 12px rgba(245,158,11,.15);'>
      <h3 style='color:#92400e;margin:0 0 12px;'>🐝 Pollinator Patrol</h3>
      <p style='color:#475569;margin:0;'>Count bees and butterflies. Study biodiversity in your area!</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Pollinator_Patrol.py", label="Start Mission →", icon="🐝")

st.markdown("---")

# ---------- Science Buddy (chat) with Dr. Curio ----------
st.markdown("""
<div style='background:linear-gradient(135deg,#e0f2fe 0%,#f0f9ff 100%);padding:24px;border-radius:20px;border:2px solid #93c5fd;margin:32px 0;'>
  <h3 style='color:#1e40af;margin:0 0 8px;'> Ask Dr.Curio (Your Science Buddy!)</h3>
  <p style='color:#475569;margin:0;'>Dr. Curio loves answering science questions! Ask anything and get friendly, accurate explanations.</p>
</div>
""", unsafe_allow_html=True)
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
st.markdown("""
<div style='text-align:center;padding:24px;background:#f8fafc;border-radius:16px;margin-top:32px;'>
  <p style='color:#64748b;margin:0;font-size:1.1rem;'>
    Built with ❤️ by <strong style='color:#3b82f6;'>CurioLab</strong> • <strong style='color:#3b82f6;'>@CURIOLAB</strong>
  </p>
  <p style='color:#94a3b8;margin:8px 0 0 0;font-size:0.9rem;'>
    Where curious minds discover science ✨
  </p>
</div>
""", unsafe_allow_html=True)
st.balloons()