import os, datetime as dt, json
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import streamlit as st

st.set_page_config(page_title="Seeds & Growth — LearnLab", page_icon="🌱", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

os.makedirs("data", exist_ok=True); os.makedirs("assets/cards", exist_ok=True)
DATA = "data/logs_seeds.csv"
if not os.path.exists(DATA):
    pd.DataFrame(columns=["date","plant","height_cm","notes"]).to_csv(DATA, index=False)

def load_df():
    df = pd.read_csv(DATA)
    if not df.empty: df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def append_row(row):
    df = load_df(); df.loc[len(df)] = row; df.to_csv(DATA, index=False)

def add_xp():
    prof = {}
    if os.path.exists("profile.json"):
        try: prof = json.load(open("profile.json","r"))
        except: prof = {}
    prof.setdefault("xp",0); prof.setdefault("streak_days",0); prof.setdefault("last_log_date", None)
    today = str(dt.date.today())
    if prof["last_log_date"]:
        last = dt.datetime.strptime(prof["last_log_date"], "%Y-%m-%d").date()
        if (dt.date.today() - last).days == 1: prof["streak_days"] += 1
    else: prof["streak_days"] = 1
    prof["last_log_date"] = today; prof["xp"] += 5
    json.dump(prof, open("profile.json","w"))

st.markdown("## 🌱 Seeds & Growth")
cute_box("Measure at the same time each day. Add notes about sunlight/water for better explanations.")

left, right = st.columns([1,2], gap="large")
with left:
    date = st.date_input("Date", value=dt.date.today())
    plant = st.text_input("Plant", value="Bean")
    height = st.number_input("Height (cm)", value=3.0, step=0.1)
    notes = st.text_area("Notes (sunlight, water, soil)", height=80)
    if st.button("Add to Seeds", type="primary"):
        append_row([str(date),plant,height,notes]); add_xp(); st.success("Added! +5 XP 🎉")
    if os.path.exists(DATA):
        st.download_button("⬇️ Download CSV", data=open(DATA,"rb").read(), file_name="logs_seeds.csv")

with right:
    df = load_df()
    st.markdown("### Your data")
    if df.empty:
        st.info("No data yet.")
    else:
        st.dataframe(df, use_container_width=True)
        fig,ax=plt.subplots(); ax.plot(pd.to_datetime(df["date"]), df["height_cm"], marker="o"); ax.set_title(f"{plant} growth"); ax.set_xlabel("Date"); ax.set_ylabel("cm"); ax.grid(True, alpha=.3); st.pyplot(fig)

        st.markdown("### Mini Science Report")
        OPENAI = os.getenv("OPENAI_API_KEY")
        if OPENAI:
            try:
                import openai; openai.api_key = OPENAI
                prompt=("Summarize plant growth. Mention 2 patterns and 1 next test. ≤100 words. Do not invent.\n\nDATA:\n"+df.to_csv(index=False))
                resp=openai.chat.completions.create(model="gpt-4o-mini",
                    messages=[{"role":"system","content":"You are a friendly science mentor."},{"role":"user","content":prompt}],
                    temperature=0.3, max_tokens=160)
                txt=resp.choices[0].message.content.strip()
            except Exception as e:
                txt=f"AI unavailable: {e}"
        else:
            txt=("**Mini Science Report**\n\n- Height increased on sunny days.\n- Consistent time helps clean curves.\n\n**Try next:** Track sunlight hours vs growth.")
        st.markdown(txt); st.text_area("Copy & share:", value=txt, height=110)

        if st.button("📜 Make Science Story Card"):
            card=Image.new("RGB",(520,720),"#fffdfc"); d=ImageDraw.Draw(card)
            d.text((24,24),"Seeds & Growth — Story Card", fill="#166534")
            body=(txt[:600]+"...") if len(txt)>600 else txt
            d.text((24,80), body, fill="#374151")
            out="assets/cards/seeds_story_card.png"; card.save(out)
            st.image(out); st.download_button("⬇️ Download Card", data=open(out,"rb").read(), file_name="Seeds_Story_Card.png")
