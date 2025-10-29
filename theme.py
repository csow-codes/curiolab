import os
import base64
import streamlit as st


PALETTE = {
    "header_text": "#5a8a9e",   # stronger pastel blue
    "body_text": "#6b7c8a",     # softer gray-blue
    "bg_light": "#f8fbfd",
    "bg_card": "#ffffff",
    "accent": "#7eb8d1",
    "border": "#e1eef5",
}


def apply_global_theme() -> None:
    """Inject global fonts and base colors with clean, modern aesthetic."""
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

/* Headers - clean Poppins */
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

/* Cards with subtle shadow */
.card {{ 
  background: {PALETTE['bg_card']}; 
  border: 1px solid {PALETTE['border']}; 
  border-radius: 20px; 
  padding: 24px;
  box-shadow: 0 2px 12px rgba(90, 138, 158, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}}

.card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(90, 138, 158, 0.12);
}}

/* Sidebar styling */
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #f0f7fb 0%, #ffffff 100%);
  border-right: 1px solid {PALETTE['border']};
}}

/* Buttons - clean and modern */
button, .stButton>button {{
  background: linear-gradient(135deg, {PALETTE['accent']} 0%, #a0cfe0 100%);
  color: #ffffff !important;
  border: none;
  border-radius: 12px;
  padding: 10px 24px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(126, 184, 209, 0.25);
}}

button:hover, .stButton>button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(126, 184, 209, 0.35);
}}

/* Hero block - cleaner, more centered */
.hero {{
  background: linear-gradient(135deg, #e8f4f8 0%, #f5fbff 100%);
  border-radius: 28px;
  padding: 48px 40px;
  margin: 16px 0 32px;
  text-align: center;
  box-shadow: 0 4px 24px rgba(90, 138, 158, 0.12);
  border: 1px solid {PALETTE['border']};
}}

.hero h1 {{ 
  margin: 0 0 12px; 
}}

.hero p {{ 
  margin: 8px 0 0 0; 
  color: {PALETTE['body_text']}; 
  font-size: 1.1rem;
  font-weight: 400;
}}

/* Mascot styling */
.hero img {{
  filter: drop-shadow(0 4px 12px rgba(90, 138, 158, 0.15));
  border-radius: 20px;
}}

/* Mission cards */
.stColumn > div {{
  padding: 12px;
}}

/* Daily challenge box */
.daily-challenge {{
  background: linear-gradient(135deg, #fff9e6 0%, #fffef5 100%);
  border-radius: 20px;
  padding: 24px;
  margin: 20px 0;
  border: 2px solid #ffe9a0;
  box-shadow: 0 2px 12px rgba(255, 200, 87, 0.15);
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
}}

a:hover {{
  color: {PALETTE['header_text']} !important;
}}

</style>
""",
        unsafe_allow_html=True,
    )


def header_with_mascot(title: str, subtitle: str = "", mascot_path: str = "assets/dr_curio.png", size_px: int = 120) -> None:
    """Render a clean hero header with mascot - inspired by modern UI."""
    img_html = ""
    if os.path.exists(mascot_path):
        b64 = base64.b64encode(open(mascot_path, "rb").read()).decode()
        img_html = f"<img src='data:image/png;base64,{{b64}}' style='width:{size_px}px;height:{size_px}px;'>"
    
    st.markdown(
        f"""
        <div class="hero">
          <div style="display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:16px;">
            {img_html}
            <h1>{title}</h1>
          </div>
          {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
