import os, datetime as dt, json
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

st.set_page_config(page_title="Air & Weather — LearnLab", page_icon="🌤️", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

os.makedirs("data", exist_ok=True); os.makedirs("assets/cards", exist_ok=True)
DATA = "data/logs_air.csv"
if not os.path.exists(DATA):
    pd.DataFrame(columns=["date","location","temperature_c","temperature_label","rainfall_mm","rainfall_label","air_quality_pm","air_quality_label","observation"]).to_csv(DATA, index=False)

def load_df():
    df = pd.read_csv(DATA)
    if not df.empty: df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def append_row(row):
    df = load_df(); df.loc[len(df)] = row; df.to_csv(DATA, index=False)

def add_xp(days=1):
    prof = {}
    if os.path.exists("profile.json"):
        try: prof = json.load(open("profile.json","r"))
        except: prof = {}
    prof.setdefault("xp",0); prof.setdefault("streak_days",0); prof.setdefault("last_log_date", None)
    today = str(dt.date.today())
    # streak logic
    if prof["last_log_date"]:
        last = dt.datetime.strptime(prof["last_log_date"], "%Y-%m-%d").date()
        if (dt.date.today() - last).days == 1:
            prof["streak_days"] += 1
    else:
        prof["streak_days"] = 1
    prof["last_log_date"] = today
    prof["xp"] += 5  # +5 XP per entry
    json.dump(prof, open("profile.json","w"))

st.markdown("## 🌤️ Air & Weather")
cute_box("Kid-friendly sliders map to numbers. Use the advanced box for exact measurements.")

left, right = st.columns([1,2], gap="large")

with left:
    st.markdown("### Add observation")
    date = st.date_input("Date", value=dt.date.today())
    location = st.text_input("Location", value="My place")
    temp_choice = st.selectbox("Temperature (feels like)", ["Cold 🧊","Mild 🙂","Warm 🌤️","Hot 🔥"])
    temp_map = {"Cold 🧊":15,"Mild 🙂":25,"Warm 🌤️":30,"Hot 🔥":35}
    rainfall_choice = st.selectbox("Rainfall", ["None ☀️","Light 🌦️","Moderate 🌧️","Heavy ⛈️"])
    rain_map = {"None ☀️":0,"Light 🌦️":2,"Moderate 🌧️":5,"Heavy ⛈️":10}
    air_choice = st.selectbox("Air quality (sky look)", ["Clear 🌈","Hazy 😐","Smoky 😷"])
    air_map = {"Clear 🌈":10,"Hazy 😐":40,"Smoky 😷":80}
    observation = st.text_area("Notes (clouds, wind, smells…)", height=80)

    temperature_c = temp_map[temp_choice]
    rainfall_mm = rain_map[rainfall_choice]
    air_pm = air_map[air_choice]

    with st.expander("Advanced numbers (optional)"):
        temperature_c = st.number_input("Exact temperature (°C)", value=float(temperature_c), step=0.1)
        rainfall_mm = st.number_input("Exact rainfall (mm)", value=float(rainfall_mm), step=0.1)
        air_pm = st.number_input("Exact PM2.5 (µg/m³)", value=float(air_pm), step=0.1)

    if st.button("Add to LearnLab", type="primary"):
        append_row([str(date),location,temperature_c,temp_choice,rainfall_mm,rainfall_choice,air_pm,air_choice,observation])
        add_xp()
        st.success("Saved! +5 XP 🎉  See your charts →")

    if os.path.exists(DATA):
        st.download_button("⬇️ Download CSV", data=open(DATA,"rb").read(), file_name="logs_air.csv")

with right:
    st.markdown("### Your data")
    df = load_df()
    if df.empty:
        st.info("No data yet.")
    else:
        st.dataframe(df.tail(200), use_container_width=True)

        # Data-quality nudge
        if len(df) >= 2:
            tmp = df.sort_values("date")
            if abs(tmp["temperature_c"].iloc[-1] - tmp["temperature_c"].iloc[-2]) > 10:
                cute_box("Heads up: today’s temperature changed >10°C from last entry. Re-check units?", bg="#fff7ed")

        st.markdown("### Charts")
        fig1, ax1 = plt.subplots(); ax1.plot(pd.to_datetime(df["date"]), df["temperature_c"], marker="o"); ax1.set_title("Temperature"); ax1.set_xlabel("Date"); ax1.set_ylabel("°C"); ax1.grid(True, alpha=.3); st.pyplot(fig1)
        fig2, ax2 = plt.subplots(); ax2.plot(pd.to_datetime(df["date"]), df["rainfall_mm"], marker="o"); ax2.set_title("Rainfall"); ax2.set_xlabel("Date"); ax2.set_ylabel("mm"); ax2.grid(True, alpha=.3); st.pyplot(fig2)
        fig3, ax3 = plt.subplots(); ax3.plot(pd.to_datetime(df["date"]), df["air_quality_pm"], marker="o"); ax3.set_title("PM2.5"); ax3.set_xlabel("Date"); ax3.set_ylabel("µg/m³"); ax3.grid(True, alpha=.3); st.pyplot(fig3)

        st.markdown("### Mini Science Report")
        OPENAI = os.getenv("OPENAI_API_KEY")
        def ai_report(rows: pd.DataFrame) -> str:
            sub = rows[["date","location","temperature_c","rainfall_mm","air_quality_pm","observation"]].copy()
            if not OPENAI:
                return ("**Mini Science Report**\n\n"
                        "- Warmest day vs rain? Any link?\n- Highest PM day: what else happened?\n\n"
                        "**Try next:** Log at the same time for one week.")
            try:
                import openai; openai.api_key = OPENAI
                SYSTEM="You are a kid-friendly science mentor. Be accurate, 120 words max."
                PROMPT=("Given [date, location, temperature_c, rainfall_mm, air_quality_pm, observation], "
                        "write 2 patterns and 1 next-week test. Do not invent data.\n\nDATA:\n"+sub.to_csv(index=False))
                resp=openai.chat.completions.create(model="gpt-4o-mini",
                    messages=[{"role":"system","content":SYSTEM},{"role":"user","content":PROMPT}],
                    temperature=0.3, max_tokens=220)
                return resp.choices[0].message.content.strip()
            except Exception as e:
                return f"AI unavailable: {e}"
        window = st.selectbox("Report window (days)", [7,14,30], index=0)
        recent = df.sort_values("date").tail(window)
        txt = ai_report(recent)
        st.markdown(txt)
        st.text_area("Copy & share:", value=txt, height=110)

        # Science Story Card
        if st.button("📜 Make Science Story Card"):
            card = Image.new("RGB", (520, 720), "#fffdfc")
            d = ImageDraw.Draw(card)
            d.text((24,24), "Air & Weather — Story Card", fill="#6b21a8")
            body = (txt[:600] + "...") if len(txt) > 600 else txt
            d.text((24, 80), body, fill="#4b5563")
            out = "assets/cards/air_story_card.png"
            card.save(out)
            st.image(out, caption="Science Story Card")
            st.download_button("⬇️ Download Card", data=open(out,"rb").read(), file_name="Air_Story_Card.png")
