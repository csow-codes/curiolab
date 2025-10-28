import os, datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Air & Weather", page_icon="🌤️", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

os.makedirs("data", exist_ok=True)
DATA_PATH = "data/logs_air.csv"
if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=["date","location","temperature_c","temperature_label","rainfall_mm","rainfall_label","air_quality_pm","air_quality_label","observation"]).to_csv(DATA_PATH, index=False)

def load_data():
    df = pd.read_csv(DATA_PATH)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def save_row(row):
    df = load_data()
    df.loc[len(df)] = row
    df.to_csv(DATA_PATH, index=False)

st.markdown("## 🌤️ Air & Weather — Local Observations")
cute_box("Kid-friendly inputs map to numbers automatically. Advanced panel lets you enter exact measurements.")

left, right = st.columns([1,2], gap="large")

with left:
    st.markdown("### Add an observation")
    date = st.date_input("Date", value=dt.date.today())
    location = st.text_input("Location (e.g., school garden)", value="My place")

    temp_choice = st.selectbox("Temperature (how did it feel?)", ["Cold 🧊","Mild 🙂","Warm 🌤️","Hot 🔥"])
    temp_map = {"Cold 🧊":15,"Mild 🙂":25,"Warm 🌤️":30,"Hot 🔥":35}
    temperature_c = temp_map[temp_choice]

    rain_choice = st.selectbox("Rainfall (how much rain?)", ["None ☀️","Light 🌦️","Moderate 🌧️","Heavy ⛈️"])
    rain_map = {"None ☀️":0,"Light 🌦️":2,"Moderate 🌧️":5,"Heavy ⛈️":10}
    rainfall_mm = rain_map[rain_choice]

    air_choice = st.selectbox("Air quality (sky look?)", ["Clear 🌈","Hazy 😐","Smoky 😷"])
    air_map = {"Clear 🌈":10,"Hazy 😐":40,"Smoky 😷":80}
    air_quality_pm = air_map[air_choice]

    observation = st.text_area("Notes (clouds, wind, smells…)", height=90)

    with st.expander("Advanced numbers (optional)"):
        temperature_c = st.number_input("Exact temperature (°C)", value=float(temperature_c), step=0.1)
        rainfall_mm = st.number_input("Exact rainfall (mm)", value=float(rainfall_mm), step=0.1)
        air_quality_pm = st.number_input("Exact PM2.5 (µg/m³)", value=float(air_quality_pm), step=0.1)

    if st.button("Add to LearnLab", type="primary"):
        save_row([str(date),location,temperature_c,temp_choice,rainfall_mm,rain_choice,air_quality_pm,air_choice,observation])
        st.success("Saved! See your charts →")

    # CSV tools
    st.markdown("#### Data tools")
    if os.path.exists(DATA_PATH):
        st.download_button("⬇️ Download CSV", data=open(DATA_PATH,"rb").read(), file_name="logs_air.csv")

with right:
    st.markdown("### Your data")
    df = load_data()
    if df.empty:
        st.info("No data yet. Add your first observation.")
    else:
        st.dataframe(df.tail(200), use_container_width=True)
        # quick nudges
        if df["date"].nunique() < df.shape[0]/2:
            cute_box("Tip: Try logging once per day around the same time for cleaner patterns ✨", bg="#fff7ed")

        st.markdown("### Charts")
        # Temperature
        fig1, ax1 = plt.subplots()
        ax1.plot(pd.to_datetime(df["date"]), df["temperature_c"], marker="o")
        ax1.set_title("Temperature over time"); ax1.set_xlabel("Date"); ax1.set_ylabel("°C")
        st.pyplot(fig1)
        # Rainfall
        fig2, ax2 = plt.subplots()
        ax2.plot(pd.to_datetime(df["date"]), df["rainfall_mm"], marker="o")
        ax2.set_title("Rainfall over time"); ax2.set_xlabel("Date"); ax2.set_ylabel("mm")
        st.pyplot(fig2)
        # PM2.5
        fig3, ax3 = plt.subplots()
        ax3.plot(pd.to_datetime(df["date"]), df["air_quality_pm"], marker="o")
        ax3.set_title("PM2.5 over time"); ax3.set_xlabel("Date"); ax3.set_ylabel("µg/m³")
        st.pyplot(fig3)

        st.markdown("### Mini Science Report")
        OPENAI_KEY = os.getenv("OPENAI_API_KEY")

        def ai_report(rows: pd.DataFrame) -> str:
            sub = rows[["date","location","temperature_c","rainfall_mm","air_quality_pm","observation"]].copy()
            if not OPENAI_KEY:
                days = sub.shape[0]
                t = round(sub["temperature_c"].astype(float).mean(),1)
                r = round(sub["rainfall_mm"].astype(float).sum(),1)
                pm = round(sub["air_quality_pm"].astype(float).mean(),1)
                return (f"**Mini Science Report**\n\n"
                        f"- You logged {days} day(s).\n"
                        f"- Avg temp: {t} °C; total rain: {r} mm; avg PM2.5: {pm}.\n"
                        f"- Look: do warm days match less rain?\n\n"
                        f"**Try next:** Compare the haziest day vs clearest day.")
            try:
                import openai
                openai.api_key = OPENAI_KEY
                SYSTEM = "You are a friendly science mentor. Keep language simple and encouraging."
                PROMPT = ("Given this table [date, location, temperature_c, rainfall_mm, air_quality_pm, observation], "
                          "write 2 patterns and 1 next-week question. 120 words max. Do not invent data.\n\nDATA:\n"
                          + sub.to_csv(index=False))
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":SYSTEM},{"role":"user","content":PROMPT}],
                    temperature=0.3, max_tokens=220
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                return f"AI unavailable: {e}\n\nTry comparing sunny vs rainy days manually."

        window = st.selectbox("Report window (days)", [7,14,30], index=0)
        recent = df.sort_values("date").tail(window)
        report_text = ai_report(recent)
        st.markdown(report_text)
        st.text_area("Copy & share this report:", value=report_text, height=120)

        st.markdown("---")
        st.subheader("Lesson: What is PM2.5?")
        st.write("PM2.5 are tiny particles that can go deep into the lungs. Lower numbers are better. On high-PM days, try to limit outdoor activity and avoid busy roads if possible.")
