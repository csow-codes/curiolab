import os
import base64
import streamlit as st


PALETTE = {
    "header_text": "#5a8a9e",
    "body_text": "#6b7c8a",
    "bg_light": "#f8fbfd",
    "bg_card": "#ffffff",
    "accent": "#7eb8d1",
    "border": "#e1eef5",
}


def apply_global_theme() -> None:
    """Inject global fonts, colors, and animations for a groundbreaking UI."""
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* Base typography */
html, body, .stApp, .stMarkdown, .stText, .stDataFrame, .stTextInput, .stButton,
.stSidebar, .stSidebar *, [class^="css"], [data-testid="stSidebar"], [data-testid="stMarkdownContainer"] * {{
  font-family: 'Poppins', system-ui, -apple-system, sans-serif !important;
  color: {PALETTE['body_text']} !important;
}}

/* Headers */
h1, h2, h3, h4, h5, h6 {{
  font-family: 'Poppins', sans-serif !important;
  font-weight: 600 !important;
  color: {PALETTE['header_text']} !important;
  letter-spacing: -0.02em;
}}

/* Hero title - pixel/coding style */
.hero h1 {{
  font-family: 'Space Mono', monospace !important;
  font-weight: 700 !important;
  color: {PALETTE['header_text']} !important;
  font-size: 3.2rem !important;
  letter-spacing: 0.05em;
  text-transform: lowercase;
}}

/* App background */
.stApp {{ 
  background: {PALETTE['bg_light']}; 
}}

/* Animated cards with breathing effect */
.card {{ 
  background: {PALETTE['bg_card']}; 
  border: 1px solid {PALETTE['border']}; 
  border-radius: 20px; 
  padding: 24px;
  box-shadow: 0 2px 12px rgba(90, 138, 158, 0.08);
  transition: all 0.3s ease;
  animation: breathe 3s ease-in-out infinite;
}}

@keyframes breathe {{
  0%, 100% {{ transform: scale(1); }}
  50% {{ transform: scale(1.02); }}
}}

.card:hover {{
  transform: translateY(-8px) scale(1.03) !important;
  box-shadow: 0 8px 30px rgba(90, 138, 158, 0.2);
  animation: none;
}}

/* Sidebar styling */
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #f0f7fb 0%, #ffffff 100%);
  border-right: 1px solid {PALETTE['border']};
}}

/* Animated XP Progress Bar */
.stProgress > div > div {{
  background: linear-gradient(90deg, #7eb8d1, #a0cfe0, #7eb8d1);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
}}

@keyframes shimmer {{
  0% {{ background-position: 200% 0; }}
  100% {{ background-position: -200% 0; }}
}}

/* Buttons with pulse effect */
button, .stButton>button {{
  background: linear-gradient(135deg, {PALETTE['accent']} 0%, #a0cfe0 100%);
  color: #ffffff !important;
  border: none;
  border-radius: 12px;
  padding: 10px 24px;
  font-weight: 500;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(126, 184, 209, 0.25);
  position: relative;
  overflow: hidden;
}}

button:hover, .stButton>button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(126, 184, 209, 0.4);
}}

button::before, .stButton>button::before {{
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}}

button:hover::before, .stButton>button:hover::before {{
  width: 300px;
  height: 300px;
}}

/* Hero block with constellation background */
.hero {{
  background: linear-gradient(135deg, #e8f4f8 0%, #f5fbff 100%);
  border-radius: 28px;
  padding: 48px 40px;
  margin: 16px 0 32px;
  text-align: center;
  box-shadow: 0 4px 24px rgba(90, 138, 158, 0.12);
  border: 1px solid {PALETTE['border']};
  position: relative;
  overflow: hidden;
}}

/* Floating particles animation */
.hero::before {{
  content: '⚗️ 🔬 🧬 🧪 ⚡ 🌟 💡 🔭';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  font-size: 24px;
  opacity: 0.15;
  animation: float 20s linear infinite;
  pointer-events: none;
  word-spacing: 60px;
  line-height: 80px;
}}

@keyframes float {{
  0% {{ transform: translateY(100%) rotate(0deg); }}
  100% {{ transform: translateY(-100%) rotate(360deg); }}
}}

.hero h1 {{ 
  margin: 0 0 12px;
  position: relative;
  z-index: 1;
}}

.hero p {{ 
  margin: 8px 0 0 0; 
  color: {PALETTE['body_text']}; 
  font-size: 1.1rem;
  font-weight: 400;
  position: relative;
  z-index: 1;
}}

/* Animated mascot bounce */
.hero img {{
  filter: drop-shadow(0 4px 12px rgba(90, 138, 158, 0.15));
  border-radius: 20px;
  animation: bounce 2s ease-in-out infinite;
  position: relative;
  z-index: 1;
}}

@keyframes bounce {{
  0%, 100% {{ transform: translateY(0); }}
  50% {{ transform: translateY(-10px); }}
}}

.hero img:hover {{
  animation: wave 0.5s ease-in-out;
}}

@keyframes wave {{
  0%, 100% {{ transform: rotate(0deg); }}
  25% {{ transform: rotate(-10deg); }}
  75% {{ transform: rotate(10deg); }}
}}

/* Flipable daily challenge card */
.daily-challenge {{
  background: linear-gradient(135deg, #fff9e6 0%, #fffef5 100%);
  border-radius: 20px;
  padding: 24px;
  margin: 20px 0;
  border: 2px solid #ffe9a0;
  box-shadow: 0 2px 12px rgba(255, 200, 87, 0.15);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}}

.daily-challenge:hover {{
  transform: rotateY(5deg) scale(1.02);
  box-shadow: 0 8px 24px rgba(255, 200, 87, 0.3);
}}

/* Mission cards */
.stColumn > div {{
  padding: 12px;
}}

/* Quick experiment button - special styling */
.quick-experiment {{
  background: linear-gradient(135deg, #ff6b9d 0%, #ffa06b 100%);
  color: white;
  padding: 16px 32px;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  box-shadow: 0 4px 20px rgba(255, 107, 157, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  animation: pulse 2s infinite;
}}

@keyframes pulse {{
  0%, 100% {{ box-shadow: 0 4px 20px rgba(255, 107, 157, 0.3); }}
  50% {{ box-shadow: 0 4px 30px rgba(255, 107, 157, 0.5); }}
}}

.quick-experiment:hover {{
  transform: scale(1.05) rotate(-2deg);
  animation: none;
}}

/* Badge styling */
.badge {{
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  border-radius: 20px;
  font-weight: 600;
  color: #8b6914;
  margin: 4px;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
  animation: badgePop 0.5s ease;
}}

@keyframes badgePop {{
  0% {{ transform: scale(0); }}
  50% {{ transform: scale(1.2); }}
  100% {{ transform: scale(1); }}
}}

/* Stats counter animation */
.stats-counter {{
  font-size: 2rem;
  font-weight: 700;
  color: {PALETTE['accent']};
  animation: countUp 1s ease-out;
}}

@keyframes countUp {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

/* Chat input styling */
.stChatInput {{
  border-radius: 16px !important;
}}

/* Links */
a {{
  color: {PALETTE['accent']} !important;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}}

a:hover {{
  color: {PALETTE['header_text']} !important;
  transform: translateX(4px);
}}

/* Streak calendar styling */
.streak-calendar {{
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  padding: 16px;
  background: {PALETTE['bg_card']};
  border-radius: 16px;
  margin: 16px 0;
}}

.streak-day {{
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s;
}}

.streak-day.active {{
  background: linear-gradient(135deg, {PALETTE['accent']} 0%, #a0cfe0 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(126, 184, 209, 0.3);
}}

.streak-day.inactive {{
  background: #f0f0f0;
  color: #ccc;
}}

.streak-day:hover {{
  transform: scale(1.1);
}}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {{
  gap: 8px;
}}

.stTabs [data-baseweb="tab"] {{
  border-radius: 12px;
  padding: 8px 20px;
  background: {PALETTE['bg_card']};
  border: 1px solid {PALETTE['border']};
  transition: all 0.3s;
}}

.stTabs [data-baseweb="tab"]:hover {{
  background: linear-gradient(135deg, {PALETTE['accent']} 0%, #a0cfe0 100%);
  color: white !important;
  transform: translateY(-2px);
}}

.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, {PALETTE['accent']} 0%, #a0cfe0 100%) !important;
  color: white !important;
  box-shadow: 0 2px 12px rgba(126, 184, 209, 0.3);
}}

/* Text input with glow effect */
.stTextInput input {{
  border-radius: 12px !important;
  border: 2px solid {PALETTE['border']} !important;
  transition: all 0.3s !important;
}}

.stTextInput input:focus {{
  border-color: {PALETTE['accent']} !important;
  box-shadow: 0 0 0 3px rgba(126, 184, 209, 0.1) !important;
}}

/* Success message animation */
.stSuccess {{
  animation: slideIn 0.3s ease;
}}

@keyframes slideIn {{
  from {{ 
    transform: translateX(-20px);
    opacity: 0;
  }}
  to {{ 
    transform: translateX(0);
    opacity: 1;
  }}
}}

/* Leaderboard hover effects */
.leaderboard-item {{
  transition: all 0.3s ease;
}}

.leaderboard-item:hover {{
  transform: translateX(8px);
  box-shadow: 0 2px 12px rgba(90, 138, 158, 0.15);
}}

/* Checklist items animation */
@keyframes checkmark {{
  0% {{ transform: scale(0) rotate(0deg); }}
  50% {{ transform: scale(1.2) rotate(180deg); }}
  100% {{ transform: scale(1) rotate(360deg); }}
}}

/* Gradient text effect for special headings */
.gradient-text {{
  background: linear-gradient(135deg, {PALETTE['accent']} 0%, #a0cfe0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

/* Floating action button style */
.fab {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b9d 0%, #ffa06b 100%);
  box-shadow: 0 4px 20px rgba(255, 107, 157, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s;
  animation: fabPulse 2s infinite;
}}

@keyframes fabPulse {{
  0%, 100% {{ 
    box-shadow: 0 4px 20px rgba(255, 107, 157, 0.4);
    transform: scale(1);
  }}
  50% {{ 
    box-shadow: 0 4px 30px rgba(255, 107, 157, 0.6);
    transform: scale(1.05);
  }}
}}

.fab:hover {{
  transform: scale(1.1) rotate(90deg) !important;
  animation: none;
}}

</style>
""",
        unsafe_allow_html=True,
    )


def header_with_mascot(title: str, subtitle: str = "", mascot_path: str = "assets/dr_curio.png", size_px: int = 120) -> None:
    """Render an animated hero header with mascot and particle effects."""
    img_html = ""
    if os.path.exists(mascot_path):
        try:
            b64 = base64.b64encode(open(mascot_path, "rb").read()).decode()
            img_html = f"<img src='data:image/png;base64,{b64}' style='width:{size_px}px;height:{size_px}px;'>"
        except Exception:
            img_html = f"<div style='font-size:{size_px}px;line-height:1;'>🧪</div>"
    else:
        img_html = f"<div style='font-size:{size_px}px;line-height:1;'>🧪</div>"
    
    st.markdown(
        f"""
        <div class="hero">
          <div style="display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:16px;position:relative;z-index:1;">
            {img_html}
            <h1>{title}</h1>
          </div>
          {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
