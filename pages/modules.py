import streamlit as st, json, os

# --- cute UI helpers ---
def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"""
        <div style="
            background-color:{bg};
            padding:12px 14px;
            border-radius:16px;
            border:1px solid #ede9fe;
            line-height:1.5;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


st.title("🗂️ Modules")

prof = {}
if os.path.exists("profile.json"):
    try:
        with open("profile.json","r") as f:
            prof = json.load(f)
        st.write(f"Hello, Dr. {prof.get('name','Scientist')}!")
        if "avatar" in prof and os.path.exists(prof["avatar"]):
            st.image(prof["avatar"], width=120)
    except Exception:
        st.info("If your profile won’t load, recreate it in Get Started.")

fav = prof.get("topics", []) if prof else []

st.write("Pick a module in the left sidebar under **Pages**.")
st.markdown("---")

mods = [
    {"title":"🌤️ Air & Weather", "desc":"Log temperature, rainfall, and PM2.5 → charts + report."},
    {"title":"🌱 Seeds & Growth", "desc":"Track plant height and see growth patterns."},
]

for m in mods:
    tag = "✅ " if (not fav or any(t in m["title"] for t in fav)) else ""
    st.markdown(f"### {tag}{m['title']}\n{m['desc']}")
