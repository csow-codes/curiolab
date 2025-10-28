import os, glob, streamlit as st, json

st.set_page_config(page_title="Modules — LearnLab", page_icon="🗂️", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

# --- helper: robust page link (works even if you tweak filenames slightly) ---
def page_link_safe(preferred_path: str, fallbacks: list[str], label: str, icon: str):
    # if preferred exists, use it
    if os.path.exists(preferred_path):
        st.page_link(preferred_path, label=label, icon=icon)
        return
    # try fallbacks (e.g., old names)
    for fb in fallbacks:
        if os.path.exists(fb):
            st.page_link(fb, label=label, icon=icon)
            return
    # final fallback: show a plain markdown link so the app still works
    st.markdown(f"**{icon} {label}** — page not found. Check filename in `pages/`.")  # gentle hint

st.markdown("## 🗂️ Modules")
cute_box("Pick any module below. Earn XP for each observation. Your streak grows when you log on consecutive days ✨")

# === Cards / links ===
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🌤️ Air & Weather")
    st.write("Log temperature, rainfall, and PM2.5. See trends + Mini Science Report.")
    page_link_safe(
        "pages/2_Air_Quality.py",
        fallbacks=["pages/2_Module_Air_Quality.py", "pages/2_air_quality.py"],
        label="Open module →",
        icon="🌤️",
    )

with c2:
    st.markdown("### 🌱 Seeds & Growth")
    st.write("Track plant height; explore how light/water affect growth.")
    page_link_safe(
        "pages/3_Seeds_Growth.py",
        fallbacks=["pages/3_Module_Seeds_Growth.py", "pages/3_seeds_growth.py"],
        label="Open module →",
        icon="🌱",
    )

with c3:
    st.markdown("### 🐝 Pollinator Patrol")
    st.write("Count bees & butterflies to study biodiversity.")
    page_link_safe(
        "pages/4_Pollinator_Patrol.py",
        fallbacks=["pages/4_Module_Pollinator_Patrol.py", "pages/4_pollinator_patrol.py"],
        label="Open module →",
        icon="🐝",
    )
