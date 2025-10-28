import os, datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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


st.title("🌤️ Air & Weather (Add Local Observations!)")

os.makedirs("data", exist_ok=True)
DATA_PATH = "data/logs_air.csv"
if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=[
        "date","location",
        "temperature_c","temperature_label",
        "rainfall_mm","rainfall_label",
        "air_quality_pm","air_quality_label",
        "observation"
    ]).to_csv(DATA_PATH, index=False)

def load_data():
    df = pd.read_csv(DATA_PATH)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def save_row(row):
    df = load_data()
    df.loc[len(df)] = row
    df.to_csv(DATA_PATH, index=False)

# Layout
left, right = st.columns([1,2])

# LEFT: Inputs
with left:
    st.subheader("Add an observation")
    date = st.date_input("Date", value=dt.date.today())
    location = st.text_input("Location (e.g., school garden, window, backyard)", value="My place")

    temp_choice = st.selectbox("Temperature (how did it feel?)", ["Cold 🧊", "Mild 🙂", "Warm 🌤️", "Hot 🔥"])
    temp_map = {"Cold 🧊":15, "Mild 🙂":25, "Warm 🌤️":30, "Hot 🔥":35}
    temperature_c = temp_map[temp_choice]

    rain_choice = st.selectbox("Rainfall (how much rain?)", ["None ☀️", "Light 🌦️", "Moderate 🌧️", "Heavy ⛈️"])
    rain_map = {"None ☀️":0, "Light 🌦️":2, "Moderate 🌧️":5, "Heavy ⛈️":10}
    rainfall_mm = rain_map[rain_choice]

    air_choice = st.selectbox("Air quality (how clear was the sky?)", ["Clear 🌈", "Hazy 😐", "Smoky 😷"])
    air_map = {"Clear 🌈":10, "Hazy 😐":40, "Smoky 😷":80}
    air_quality_pm = air_map[air_choice]

    observation = st.text_area("What did you notice? (smells, clouds, wind, sounds, etc.)", height=100)

    if st.button("Add to LearnLab"):
        save_row([
            str(date), location,
            temperature_c, temp_choice,
            rainfall_mm, rain_choice,
            air_quality_pm, air_choice,
            observation
        ])
        st.success("Saved! Scroll right to see charts and your report.")

# RIGHT: charts + report
with right:
    st.subheader("Your data")
    df = load_data()

    if df.empty:
        st.info("No data yet. Add your first observation on the left.")
    else:
        st.dataframe(df.tail(100), use_container_width=True)

        st.subheader("Charts")

        fig1, ax1 = plt.subplots()
        ax1.plot(pd.to_datetime(df["date"]), df["temperature_c"], marker="o")
        ax1.set_title("Temperature over time")
        ax1.set_xlabel("Date"); ax1.set_ylabel("°C (mapped from feeling)")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        ax2.plot(pd.to_datetime(df["date"]), df["rainfall_mm"], marker="o")
        ax2.set_title("Rainfall over time")
        ax2.set_xlabel("Date"); ax2.set_ylabel("mm (mapped from ‘None/Light/…’)")
        st.pyplot(fig2)

        fig3, ax3 = plt.subplots()
        ax3.plot(pd.to_datetime(df["date"]), df["air_quality_pm"], marker="o")
        ax3.set_title("PM2.5 over time")
        ax3.set_xlabel("Date"); ax3.set_ylabel("µg/m³ (mapped from ‘Clear/Hazy/Smoky’)")
        st.pyplot(fig3)

        st.subheader("Mini Science Report")

        OPENAI_KEY = os.getenv("OPENAI_API_KEY")

        def ai_report(rows: pd.DataFrame) -> str:
            sub = rows[["date","location","temperature_c","rainfall_mm","air_quality_pm","observation"]]
            if not OPENAI_KEY:
                days = sub.shape[0]
                t = round(sub["temperature_c"].mean(), 1)
                r = round(sub["rainfall_mm"].sum(), 1)
                pm = round(sub["air_quality_pm"].mean(), 1)
                return (f"**Mini Science Report**\n\n"
                        f"- You logged {days} day(s).\n"
                        f"- Avg temperature: {t} °C. Total rain: {r} mm. Avg PM2.5: {pm}.\n"
                        f"- Notice: do warmer days line up with less rain?\n\n"
                        f"**Try next:** What changed on the haziest day?")
            try:
                import openai
                openai.api_key = OPENAI_KEY
                SYSTEM = "You are a friendly science mentor. Keep language simple and encouraging."
                PROMPT = ("Given this small table of observations with columns "
                          "[date, location, temperature_c, rainfall_mm, air_quality_pm, observation], "
                          "write 2 patterns and 1 question to investigate next week. 120 words max.\n\nDATA:\n"
                          + sub.to_csv(index=False))
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":SYSTEM},
                              {"role":"user","content":PROMPT}],
                    temperature=0.3, max_tokens=220
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                return f"AI unavailable ({e}). Look for patterns manually."

        window = st.selectbox("Report window (days)", [7,14,30], index=0)
        recent = df.sort_values("date").tail(window)
        st.markdown(ai_report(recent))

        st.markdown("---")
        st.subheader("Lesson: What is PM2.5?")
        st.write(
            "PM2.5 are tiny particles in the air that can go deep into the lungs. "
            "Lower numbers are better. On high-PM days, try to limit outdoor activity."
        )
