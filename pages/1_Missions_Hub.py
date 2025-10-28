import streamlit as st, os, json, pandas as pd, datetime as dt

st.set_page_config(page_title="Missions — LearnLab", page_icon="🧭", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

def count_rows(path): 
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

st.markdown("## 🧭 Missions")
cute_box("Complete missions to earn XP and badges. Explore → Explain → Share.")

air_rows = count_rows("data/logs_air.csv")
seed_rows = count_rows("data/logs_seeds.csv")
pol_rows = count_rows("data/logs_pollinators.csv")

c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("### 🌤️ Air & Weather")
    st.write(f"{air_rows} observations")
    st.page_link("pages/2_Air_Quality.py", label="Open module →", icon="🌤️")
with c2:
    st.markdown("### 🌱 Seeds & Growth")
    st.write(f"{seed_rows} observations")
    st.page_link("pages/3_Seeds_Growth.py", label="Open module →", icon="🌱")
with c3:
    st.markdown("### 🐝 Pollinator Patrol")
    st.write(f"{pol_rows} observations")
    st.page_link("pages/4_Pollinator_Patrol.py", label="Open module →", icon="🐝")

st.markdown("---")
st.subheader("🎓 Teacher & Coach")
colA, colB = st.columns(2)
with colA:
    st.write("Download CSV logs:")
    if os.path.exists("data/logs_air.csv"): st.download_button("⬇️ Air & Weather CSV", data=open("data/logs_air.csv","rb").read(), file_name="logs_air.csv")
    if os.path.exists("data/logs_seeds.csv"): st.download_button("⬇️ Seeds & Growth CSV", data=open("data/logs_seeds.csv","rb").read(), file_name="logs_seeds.csv")
    if os.path.exists("data/logs_pollinators.csv"): st.download_button("⬇️ Pollinators CSV", data=open("data/logs_pollinators.csv","rb").read(), file_name="logs_pollinators.csv")
with colB:
    st.write("Quick feedback (1–2 questions)")
    ease = st.slider("How easy was LearnLab to use?", 1, 5, 4)
    conf = st.slider("Do the charts make sense?", 1, 5, 4)
    msg  = st.text_input("One thing to improve", "")
    if st.button("Submit feedback"):
        os.makedirs("data", exist_ok=True)
        with open("data/feedback.csv","a") as f:
            f.write(f"{str(dt.date.today())},{ease},{conf},{msg}\n")
        st.success("Thanks! ✨")
    if os.path.exists("data/feedback.csv"):
        fb = pd.read_csv("data/feedback.csv", header=None, names=["date","ease","conf","msg"])
        st.caption(f"Feedback so far — ease: {fb['ease'].mean():.1f}/5, understanding: {fb['conf'].mean():.1f}/5 (n={len(fb)})")
