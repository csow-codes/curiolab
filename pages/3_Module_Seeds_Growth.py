import os, datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Seeds & Growth", page_icon="🌱", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

os.makedirs("data", exist_ok=True)
DATA = "data/logs_seeds.csv"
if not os.path.exists(DATA):
    pd.DataFrame(columns=["date","plant","height_cm","notes"]).to_csv(DATA, index=False)

def load_df():
    df = pd.read_csv(DATA)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def append_row(row):
    df = load_df()
    df.loc[len(df)] = row
    df.to_csv(DATA, index=False)

st.markdown("## 🌱 Seeds & Growth — Plant Height Tracker")
cute_box("Measure at the same time each day for smooth curves. Add sunlight/water notes to explain jumps.")

left, right = st.columns([1,2], gap="large")

with left:
    st.markdown("### Add observation")
    date = st.date_input("Date", value=dt.date.today())
    plant = st.text_input("Plant name", value="Bean")
    height = st.number_input("Height (cm)", value=3.0, step=0.1)
    notes = st.text_area("Notes (sunlight, water, soil, etc.)", height=80)
    if st.button("Add to Seeds", type="primary"):
        append_row([str(date), plant, height, notes])
        st.success("Added!")

    if os.path.exists(DATA):
        st.download_button("⬇️ Download CSV", data=open(DATA,"rb").read(), file_name="logs_seeds.csv")

with right:
    st.markdown("### Your data")
    df = load_df()
    if df.empty:
        st.info("No data yet.")
    else:
        st.dataframe(df, use_container_width=True)
        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(df["date"]), df["height_cm"], marker="o")
        ax.set_title(f"{plant} growth over time")
        ax.set_xlabel("Date"); ax.set_ylabel("Height (cm)")
        st.pyplot(fig)

        st.markdown("### Mini Science Report")
        OPENAI = os.getenv("OPENAI_API_KEY")
        if OPENAI:
            try:
                import openai
                openai.api_key = OPENAI
                prompt = ("Summarize plant growth. Mention 2 patterns and 1 test for next week. "
                          "≤100 words. Do not invent data.\n\nDATA:\n" + df.to_csv(index=False))
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":"You are a friendly science mentor."},
                              {"role":"user","content":prompt}],
                    temperature=0.3, max_tokens=160
                )
                txt = resp.choices[0].message.content.strip()
                st.markdown(txt); st.text_area("Copy & share:", value=txt, height=110)
            except Exception as e:
                st.write(f"AI unavailable: {e}")
        else:
            txt = ("**Mini Science Report**\n\n"
                   "- Height increased across days; biggest jump followed a sunny day.\n"
                   "- Try measuring at the same hour daily.\n\n"
                   "**Try next:** Track sunlight hours vs growth.")
            st.markdown(txt); st.text_area("Copy & share:", value=txt, height=110)

st.markdown("---")
st.subheader("Lesson: How do plants grow?")
st.write("Plants use sunlight, water, and nutrients from soil. They make food in leaves (photosynthesis) and use it to build stems and roots.")
