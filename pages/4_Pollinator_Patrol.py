import os, datetime as dt, json
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import streamlit as st

st.set_page_config(page_title="Pollinator Patrol — LearnLab", page_icon="🐝", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>", unsafe_allow_html=True)

os.makedirs("data", exist_ok=True); os.makedirs("assets/cards", exist_ok=True)
DATA = "data/logs_pollinators.csv"
if not os.path.exists(DATA):
    pd.DataFrame(columns=["date","location","bees","butterflies","flowers","weather","notes"]).to_csv(DATA, index=False)

def load_df():
    df = pd.read_csv(DATA)
    if not df.empty: df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def append_row(row):
    df = load_df(); df.loc[len(df)] = row; df.to_csv(DATA, index=False)

def add_xp():
    prof={}
    if os.path.exists("profile.json"):
        try: prof=json.load(open("profile.json","r"))
        except: prof={}
    prof.setdefault("xp",0); prof.setdefault("streak_days",0); prof.setdefault("last_log_date", None)
    today=str(dt.date.today())
    if prof["last_log_date"]:
        last=dt.datetime.strptime(prof["last_log_date"], "%Y-%m-%d").date()
        if (dt.date.today() - last).days == 1: prof["streak_days"] += 1
    else: prof["streak_days"]=1
    prof["last_log_date"]=today; prof["xp"] += 5
    json.dump(prof, open("profile.json","w"))

st.markdown("## 🐝 Pollinator Patrol")
cute_box("Observe for **10 minutes**. Count bees & butterflies. Be gentle — no disturbing 🐝🦋")

left,right=st.columns([1,2], gap="large")
with left:
    date=st.date_input("Date", value=dt.date.today())
    location=st.text_input("Location", value="School garden")
    bees=st.slider("Bees (10 min)", 0, 30, 3)
    butterflies=st.slider("Butterflies (10 min)", 0, 30, 1)
    flowers=st.selectbox("Flower bloom", ["None 🌿","Some 🌸","Lots 🌺"])
    weather=st.selectbox("Weather", ["Sunny ☀️","Cloudy ☁️","Windy 🍃","Rainy 🌧️"])
    notes=st.text_area("Notes", height=80)

    if st.button("Add to Patrol", type="primary"):
        append_row([str(date),location,bees,butterflies,flowers,weather,notes]); add_xp()
        st.success("Saved! +5 XP 🎉")
    if os.path.exists(DATA):
        st.download_button("⬇️ Download CSV", data=open(DATA,"rb").read(), file_name="logs_pollinators.csv")

with right:
    df=load_df(); st.markdown("### Your data")
    if df.empty: st.info("No data yet.")
    else:
        st.dataframe(df.tail(200), use_container_width=True)
        fig1,ax1=plt.subplots(); ax1.plot(pd.to_datetime(df["date"]), df["bees"], marker="o"); ax1.set_title("Bees over time"); ax1.set_xlabel("Date"); ax1.set_ylabel("Count"); ax1.grid(True, alpha=.3); st.pyplot(fig1)
        fig2,ax2=plt.subplots(); ax2.plot(pd.to_datetime(df["date"]), df["butterflies"], marker="o"); ax2.set_title("Butterflies over time"); ax2.set_xlabel("Date"); ax2.set_ylabel("Count"); ax2.grid(True, alpha=.3); st.pyplot(fig2)

        st.markdown("#### Averages by condition")
        st.dataframe(df.groupby("weather")[["bees","butterflies"]].mean().round(1))
        st.dataframe(df.groupby("flowers")[["bees","butterflies"]].mean().round(1))

        st.markdown("### Mini Science Report")
        OPENAI=os.getenv("OPENAI_API_KEY")
        if OPENAI:
            try:
                import openai; openai.api_key=OPENAI
                prompt=("Using [date, location, bees, butterflies, flowers, weather, notes], "
                        "write 2 patterns and 1 next question. ≤120 words.\n\nDATA:\n"+df.to_csv(index=False))
                resp=openai.chat.completions.create(model="gpt-4o-mini",
                    messages=[{"role":"system","content":"You are a friendly science mentor."},{"role":"user","content":prompt}],
                    temperature=0.3, max_tokens=220)
                txt=resp.choices[0].message.content.strip()
            except Exception as e:
                txt=f"AI unavailable: {e}"
        else:
            txt=("**Mini Science Report**\n\n- More visitors on sunny days.\n- More flowers → more pollinators.\n\n**Try next:** Observe at the same time daily.")
        st.markdown(txt); st.text_area("Copy & share:", value=txt, height=110)

        if st.button("📜 Make Science Story Card"):
            card=Image.new("RGB",(520,720),"#fffdfc"); d=ImageDraw.Draw(card)
            d.text((24,24),"Pollinator Patrol — Story Card", fill="#854d0e")
            body=(txt[:600]+"...") if len(txt)>600 else txt
            d.text((24,80), body, fill="#374151")
            out="assets/cards/pollinator_story_card.png"; card.save(out)
            st.image(out); st.download_button("⬇️ Download Card", data=open(out,"rb").read(), file_name="Pollinator_Story_Card.png")
