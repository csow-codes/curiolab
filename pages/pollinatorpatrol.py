import os, datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("🐝 Pollinator Patrol — Bees & Butterflies")
st.caption("Count friendly pollinators to help your garden science!")

# optional cute intro
def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"<div style='background-color:{bg};padding:12px;border-radius:16px;border:1px solid #ede9fe'>{text}</div>",
        unsafe_allow_html=True
    )
cute_box("Look for bees 🐝 and butterflies 🦋 for **10 minutes**. Be gentle and don’t disturb them!")

os.makedirs("data", exist_ok=True)
DATA = "data/logs_pollinators.csv"
if not os.path.exists(DATA):
    pd.DataFrame(columns=["date","location","bees","butterflies","flowers","weather","notes"]).to_csv(DATA, index=False)

def load_df():
    df = pd.read_csv(DATA)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def append_row(row):
    df = load_df()
    df.loc[len(df)] = row
    df.to_csv(DATA, index=False)

left, right = st.columns([1,2])

with left:
    st.subheader("Add observation")
    date = st.date_input("Date", value=dt.date.today())
    location = st.text_input("Location", value="School garden")
    # kid-friendly counts (0–10 range)
    bees = st.slider("Bees seen (10 min)", 0, 20, 2)
    butterflies = st.slider("Butterflies seen (10 min)", 0, 20, 1)
    flowers = st.selectbox("Flower bloom level", ["None 🌿","Some 🌸","Lots 🌺"])
    weather = st.selectbox("Weather", ["Sunny ☀️","Cloudy ☁️","Windy 🍃","Rainy 🌧️"])
    notes = st.text_area("Notes (colors, plants, time of day)", height=80)

    if st.button("Add to Patrol"):
        append_row([str(date), location, bees, butterflies, flowers, weather, notes])
        st.success("Saved! Check your patterns →")

with right:
    st.subheader("Your data")
    df = load_df()
    if df.empty:
        st.info("No data yet. Log your first patrol on the left.")
    else:
        st.dataframe(df.tail(100), use_container_width=True)

        st.subheader("Charts")
        fig1, ax1 = plt.subplots()
        ax1.plot(pd.to_datetime(df["date"]), df["bees"], marker="o")
        ax1.set_title("Bees over time"); ax1.set_xlabel("Date"); ax1.set_ylabel("Count (10 min)")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        ax2.plot(pd.to_datetime(df["date"]), df["butterflies"], marker="o")
        ax2.set_title("Butterflies over time"); ax2.set_xlabel("Date"); ax2.set_ylabel("Count (10 min)")
        st.pyplot(fig2)

        st.subheader("Mini Science Report")
        OPENAI_KEY = os.getenv("OPENAI_API_KEY")
        subset = df[["date","location","bees","butterflies","flowers","weather","notes"]].copy()

        def report(rows: pd.DataFrame) -> str:
            if not OPENAI_KEY:
                return ("**Mini Science Report**\n\n"
                        "- Do you see more pollinators on sunny days?\n"
                        "- Do counts go up when there are **lots of flowers**?\n\n"
                        "**Try next:** Observe at the same time of day for a week.")
            try:
                import openai, io
                openai.api_key = OPENAI_KEY
                SYSTEM = "You are a friendly science mentor. Keep language simple and encouraging."
                PROMPT = ("Given this small table of pollinator observations with columns "
                          "[date, location, bees, butterflies, flowers, weather, notes], "
                          "write 2 patterns and 1 next question. 120 words max.\n\nDATA:\n"
                          + rows.to_csv(index=False))
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":SYSTEM},
                              {"role":"user","content":PROMPT}],
                    temperature=0.3, max_tokens=220
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                return f"AI unavailable: {e}. Look for sunny vs cloudy patterns manually."

        window = st.selectbox("Report window (days)", [7,14,30], index=0)
        recent = df.sort_values("date").tail(window)
        st.markdown(report(recent))

        st.markdown("---")
        st.subheader("Lesson: Why pollinators matter 🐝")
        st.write("Pollinators help plants make seeds and fruits. More flowers usually means more visitors. "
                 "Wind and rain can lower activity. Try to observe at the same time each day.")
