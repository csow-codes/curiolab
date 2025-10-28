import streamlit as st, json, os, pandas as pd

st.set_page_config(page_title="Modules b", page_icon="🗂️", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json","r"))
    except Exception:
        prof = {}

st.markdown("## 🗂️ Modules")
cute_box("Pick any module below. Earn XP for each observation. Your streak grows when you log on consecutive days ✨")

# quick stats
def count_rows(path): 
    return pd.read_csv(path).shape[0] if os.path.exists(path) else 0

air_rows = count_rows("data/logs_air.csv")
seed_rows = count_rows("data/logs_seeds.csv")
pol_rows = count_rows("data/logs_pollinators.csv")

c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("### 🌤️ Air & Weather")
    st.write(f"{air_rows} observations")
    st.page_link("pages/2_Module_Air_Quality.py", label="Open module →", icon="🌤️")
with c2:
    st.markdown("### 🌱 Seeds & Growth")
    st.write(f"{seed_rows} observations")
    st.page_link("pages/3_Module_Seeds_Growth.py", label="Open module →", icon="🌱")
with c3:
    st.markdown("### 🐝 Pollinator Patrol")
    st.write(f"{pol_rows} observations")
    try:
        st.page_link("pages/4_Module_Pollinator_Patrol.py", label="Open module →", icon="🐝")
    except Exception:
        st.info("Add `pages/4_Module_Pollinator_Patrol.py` to enable.")

st.markdown("---")
st.markdown("### 🎁 Teacher/Mentor tools")
colA, colB = st.columns(2)
with colA:
    # export all CSVs zipped? keep simple: offer links individually
    st.write("Download CSV logs:")
    if os.path.exists("data/logs_air.csv"): st.download_button("⬇️ Air & Weather CSV", data=open("data/logs_air.csv","rb").read(), file_name="logs_air.csv")
    if os.path.exists("data/logs_seeds.csv"): st.download_button("⬇️ Seeds & Growth CSV", data=open("data/logs_seeds.csv","rb").read(), file_name="logs_seeds.csv")
    if os.path.exists("data/logs_pollinators.csv"): st.download_button("⬇️ Pollinators CSV", data=open("data/logs_pollinators.csv","rb").read(), file_name="logs_pollinators.csv")
with colB:
    st.write("Load sample datasets (for demos)")
    if st.button("📥 Load sample data"):
        os.makedirs("data", exist_ok=True)
        # minimal small samples
        import datetime as dt
        import pandas as pd
        pd.DataFrame([
            [str(dt.date.today()), "School", 28, "Warm 🌤️", 0, "None ☀️", 18, "Clear 🌈", "Clouds in the pm"],
            [str(dt.date.today()-dt.timedelta(days=1)), "School", 26,"Mild 🙂", 2,"Light 🌦️", 35,"Hazy 😐","Windy"],
        ], columns=["date","location","temperature_c","temperature_label","rainfall_mm","rainfall_label","air_quality_pm","air_quality_label","observation"]).to_csv("data/logs_air.csv",index=False)
        pd.DataFrame([
            [str(dt.date.today()-dt.timedelta(days=2)),"Bean",3.0,"sprout"], 
            [str(dt.date.today()-dt.timedelta(days=1)),"Bean",4.2,"sunny"], 
            [str(dt.date.today()),"Bean",5.1,"watered"]
        ], columns=["date","plant","height_cm","notes"]).to_csv("data/logs_seeds.csv",index=False)
        pd.DataFrame([
            [str(dt.date.today()-dt.timedelta(days=1)),"Garden",3,1,"Lots 🌺","Sunny ☀️","no wind"],
            [str(dt.date.today()),"Garden",5,2,"Lots 🌺","Sunny ☀️","noon"]
        ], columns=["date","location","bees","butterflies","flowers","weather","notes"]).to_csv("data/logs_pollinators.csv",index=False)
        st.success("Sample data loaded! Open modules to see charts.")
