import os
import base64
import streamlit as st


PALETTE = {
    "header_text": "#7c9aa8",   # pastel blue-gray for headers
    "body_text": "#a4a4a4",     # soft gray for body
    "bg_light": "#ffffff",
    "bg_card": "#f6f9fb",
    "accent": "#a7c7d6",       # pastel accent
}


def apply_global_theme() -> None:
    """Inject global fonts and base colors, including sidebar and navigation.
    Ensures consistency when navigating across Streamlit pages.
    """
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');

/* Base typography everywhere */
html, body, .stApp, .stMarkdown, .stText, .stDataFrame, .stTextInput, .stButton,
.stSidebar, .stSidebar * , [class^="css"], [data-testid="stSidebar"], [data-testid="stMarkdownContainer"] * {
  font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif !important;
  color: {PALETTE['body_text']} !important;
}

h1, h2, h3, h4, h5, h6, .hero h1, .hero h2, .hero h3 {
  font-family: 'Nunito', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif !important;
  font-weight: 900 !important; /* ExtraBold */
  color: {PALETTE['header_text']} !important;
}

/* App background and cards */
.stApp {{ background: {PALETTE['bg_light']}; }}
.card {{ background: {PALETTE['bg_card']}; border: 1px solid #e8eef2; border-radius: 16px; padding: 20px; }}

/* Sidebar look */
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #eef6fa 0%, #ffffff 100%);
  border-right: 1px solid #e5eef3;
}}

/* Buttons */
button, .stButton>button {{
  background: linear-gradient(135deg, #d8eaf3 0%, #eef6fa 100%);
  color: #40606e; border: 1px solid #d1e4ee; border-radius: 10px;
}}

/* Hero block base style */
.hero{{
  background: linear-gradient(135deg,#e8f3f8 0%, #f6fbff 50%, #ffffff 100%);
  border-radius: 24px; padding: 32px 40px; margin: 8px 0 24px; text-align:center;
  box-shadow: 0 8px 20px rgba(124,154,168,0.18);
  border: 1px solid #dce9f0;
}}
.hero h1{{ margin: 0 0 8px; font-size: 2.6rem; }}
.hero p{{ margin: 6px 0 0 0; color: {PALETTE['body_text']}; }}

</style>
""",
        unsafe_allow_html=True,
    )


def header_with_mascot(title: str, subtitle: str = "", mascot_path: str = "assets/dr_curio.png", size_px: int = 84) -> None:
    """Render a hero header with the Dr. Curio mascot image if available.
    The mascot appears in the hero (not in the sidebar).
    """
    img_html = ""
    if os.path.exists(mascot_path):
        b64 = base64.b64encode(open(mascot_path, "rb").read()).decode()
        img_html = f"<img src='data:image/png;base64,{b64}' style='width:{size_px}px;height:{size_px}px;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
    st.markdown(
        f"""
        <div class="hero">
          <div style="display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;">
            {img_html}
            <h1>{title}</h1>
          </div>
          {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


