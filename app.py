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

st.set_page_config(page_title="LearnLab", layout="wide")
st.title("LearnLab: Science for Everyone")
st.caption("Turn any place into a mini research lab.")

# Load profile if exists
prof = {}
if os.path.exists("profile.json"):
    try:
        with open("profile.json", "r") as f:
            prof = json.load(f)
        st.success(f"Welcome back, Dr. {prof.get('name','Scientist')}! 🎉")
    except Exception:
        st.warning("Profile file unreadable. You can recreate it in Get Started → Profile.")

st.header("Get started")
st.markdown("1️⃣ Open **Get Started → Profile** to set your name, avatar, and interests.")
st.markdown("2️⃣ Visit **Modules** and pick a topic.")
st.markdown("3️⃣ Try **Air & Weather** first — it’s ready to use.")

st.markdown("---")
st.subheader("About LearnLab")
st.write(
    "LearnLab makes science hands-on in any place. Students record real-world data, see charts, "
    "and get a Mini Science Report. It’s designed for any setting with friendly inputs, "
    "local files, and simple visuals."
)
