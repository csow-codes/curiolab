import os, datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st, json, os

# Home page
st.set_page_config(page_title="LearnLab", layout="wide")
st.title("LearnLab: Science for Everyone")
st.caption("Turn any place into a mini research lab!")

# Load profile (if exists)
prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json"))
        st.success(f"Welcome back, Dr. {prof.get('name','Scientist')}! 🎉")
    except Exception:
        st.warning("Profile file unreadable. You can recreate it in Get Started → Profile.")

st.header("Get started")
st.markdown("1) Open **Get Started → Profile** to set your name, avatar, and interests.")
st.markdown("2) Visit **Modules** and pick a topic.")
st.markdown("3) Try **Air & Weather** first (temperature, rainfall, PM2.5) — it's ready.")

st.markdown("---")
st.subheader("About LearnLab")
st.write(
    "LearnLab makes science hands-on in any classroom. Log observations, see charts, and get a "
    "plain-language Mini Science Report (with or without AI). It's designed for **low-resource** settings: "
    "friendly inputs, local files, and simple visuals."
)

#setup the page
st.set_page_config(page_title="LearnLab", layout="wide") #browser tab title and wide layout
st.title("LearnLab: Science For Everyone") #big page title
st.caption("Log your observations, see patterns, and get a plain-language Mini Science Report.") #subtitle

#create data file
DATA_PATH = "data.csv" #CSV file where entries will be stored
if not os.path.exists(DATA_PATH): #if it's the first run and the file doesn't yet exist
    #make an empty table with the six columns we need and save it as data.csv
    pd.DataFrame(columns=[
        "data","location","temperature_f","temperature_label","rainfall_mm","rainfall_label","air_quality_pm","air_quality_label","observation"
    ]).to_csv(DATA_PATH, index=False)

#Get Started!
import streamlit as st, json, os, random
from PIL import Image, ImageDraw

st.title("👩‍🔬 Get Started — Create Your Scientist Profile")

name = st.text_input("Your name or nickname", value="Alex")
age = st.selectbox("Age range", ["8–10","11–13","14–16"])
topics = st.multiselect("Favorite topics", ["Environment","Plants","Weather","Health","Physics","Space"])

# Simple mirrored pixel avatar generator (no external APIs)
def generate_avatar(seed_text="Alex", size=8, scale=22):
    random.seed(seed_text)
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    colors = [(55,148,255), (80,200,120), (250,180,70), (165,120,255)]
    for y in range(size):
        for x in range(size//2):
            c = random.choice(colors) if random.random() > 0.35 else (240,240,240)
            draw.point((x, y), fill=c)
            draw.point((size-1-x, y), fill=c)  # mirror
    img = img.resize((size*scale, size*scale), Image.NEAREST)
    return img

st.write("Preview avatar:")
avatar = generate_avatar(name)
st.image(avatar, caption="Your scientist avatar", use_container_width=False)

if st.button("Save Profile"):
    os.makedirs("assets/avatars", exist_ok=True)
    avatar_path = f"assets/avatars/{name.lower().replace(' ','_')}.png"
    avatar.save(avatar_path)
    json.dump({"name": name, "age": age, "topics": topics, "avatar": avatar_path}, open("profile.json","w"))
    st.success("Profile saved! Open the Modules page to pick a topic.")

#Modules
import streamlit as st, json, os

st.title("🗂️ Modules")

prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json"))
        st.write(f"Hello, Dr. {prof.get('name','Scientist')}!")
        if "avatar" in prof and os.path.exists(prof["avatar"]):
            st.image(prof["avatar"], width=120)
    except Exception:
        st.info("Tip: If your profile won’t load, recreate it in Get Started.")

fav = prof.get("topics", []) if prof else []

st.write("Pick a module in the sidebar (“Pages”). Suggested first: **Air & Weather**.")
st.markdown("---")

mods = [
    {"title":"Air & Weather", "desc":"Log temperature, rainfall, PM2.5 → charts + Mini Science Report."},
    {"title":"Seeds & Growth", "desc":"Track plant height over days and see growth patterns."},
]

for m in mods:
    tag = "✅ " if (not fav or any(t in m["title"] for t in fav)) else ""
    st.markdown(f"### {tag}{m['title']}\n{m['desc']}")

def load_data():
    df = pd.read_csv(DATA_PATH)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        return df

def save_row(row):
    df = load_data()
    df.loc[len(df)]=row
    df.to_csv(DATA_PATH,index=False)

#Layout
left,right = st.columns([1,2])

#Form (on the left)
with left:
    st.subheader("Add an observation")

    #basic fields
    data = st.date_input("Date", value=dt.date.today())
    location = st.text_input("Location (e.g., school garden, window, backyard)",value="My place")

    # qualitative → quantitative mappings
    temp_choice = st.selectbox("Temperature (how did it feel?)", ["Cold 🧊", "Mild 🙂", "Warm 🌤️", "Hot 🔥"])
    temp_map = {"Cold 🧊":15, "Mild 🙂":25, "Warm 🌤️":30, "Hot 🔥":35}
    temperature_f = temp_map[temp_choice]

    rain_choice = st.selectbox("Rainfall (how much rain?)", ["None ☀️", "Light 🌦️", "Moderate 🌧️", "Heavy ⛈️"])
    rain_map = {"None ☀️":0, "Light 🌦️":2, "Moderate 🌧️":5, "Heavy ⛈️":10}
    rainfall_mm = rain_map[rain_choice]

    air_choice = st.selectbox("Air quality (how clear was the sky?)", ["Clear 🌈", "Hazy 😐", "Smoky 😷"])
    air_map = {"Clear 🌈":10, "Hazy 😐":40, "Smoky 😷":80}
    air_quality_pm = air_map[air_choice]

    observation = st.text_area("What did you notice? (smells, clouds, wind, sounds, etc.)", height=100)

    # optional: let advanced users enter exact numbers
    with st.expander("Advanced: enter exact numbers (optional)"):
        exact_temp = st.number_input("Exact temperature (°F)", value=float(temperature_f), step=0.1)
        exact_rain = st.number_input("Exact rainfall (mm)", value=float(rainfall_mm), step=0.1)
        exact_pm = st.number_input("Exact PM2.5 (µg/m³)", value=float(air_quality_pm), step=0.1)
        # if they change the exact values, use them
        temperature_f = exact_temp
        rainfall_mm = exact_rain
        air_quality_pm = exact_pm

    if st.button("Add to LearnLab"):
        save_row([
            str(date), location,
            temperature_f, temp_choice,
            rainfall_mm, rain_choice,
            air_quality_pm, air_choice,
            observation
        ])
        st.success("Saved! Scroll right to see charts and your report.")

# ---------- RIGHT: table, charts, report ----------
with right:
    st.subheader("Your data")
    df = load_data()

    if df.empty:
        st.info("No data yet. Add your first observation on the left.")
    else:
        # Show labels too so it’s transparent how numbers came from words
        st.dataframe(df.tail(100), use_container_width=True)

        st.subheader("Charts")

        # Temperature
        fig1, ax1 = plt.subplots()
        ax1.plot(pd.to_datetime(df["date"]), df["temperature_f"], marker="o")
        ax1.set_title("Temperature over time")
        ax1.set_xlabel("Date"); ax1.set_ylabel("°C (mapped from feeling)")
        st.pyplot(fig1)

        # Rainfall
        fig2, ax2 = plt.subplots()
        ax2.plot(pd.to_datetime(df["date"]), df["rainfall_mm"], marker="o")
        ax2.set_title("Rainfall over time")
        ax2.set_xlabel("Date"); ax2.set_ylabel("mm (mapped from ‘None/Light/…’)")
        st.pyplot(fig2)

        # PM2.5
        fig3, ax3 = plt.subplots()
        ax3.plot(pd.to_datetime(df["date"]), df["air_quality_pm"], marker="o")
        ax3.set_title("PM2.5 over time")
        ax3.set_xlabel("Date"); ax3.set_ylabel("µg/m³ (mapped from ‘Clear/Hazy/Smoky’)")
        st.pyplot(fig3)

        # ---------- Mini Science Report ----------
        st.subheader("Mini Science Report")

        OPENAI_KEY = os.getenv("OPENAI_API_KEY")

        def ai_report(rows: pd.DataFrame) -> str:
            # Always use the numeric columns; labels are there for transparency
            sub = rows[["date","location","temperature_f","rainfall_mm","air_quality_pm","observation"]].copy()

            if not OPENAI_KEY:
                # fallback: simple stats + a thinking prompt
                days = sub.shape[0]
                t = round(sub["temperature_f"].astype(float).mean(), 1)
                r = round(sub["rainfall_mm"].astype(float).sum(), 1)
                pm = round(sub["air_quality_pm"].astype(float).mean(), 1)
                return (f"**Mini Science Report**\n\n"
                        f"- You logged {days} day(s).\n"
                        f"- Avg temperature: {t} °C. Total rain: {r} mm. Avg PM2.5: {pm}.\n"
                        f"- Try to notice: do warmer days line up with less rain?\n\n"
                        f"**Try investigating next:** What changed on the haziest (highest PM) day?")

            # AI version
            import openai
            openai.api_key = OPENAI_KEY
            SYSTEM = "You are a friendly science mentor. Keep language simple and encouraging."
            PROMPT = ("Given this small table of observations with columns "
                      "[date, location, temperature_f, rainfall_mm, air_quality_pm, observation], "
                      "write 2 simple patterns you notice and 1 question to investigate next week. "
                      "120 words max. Do not invent data.\n\nDATA:\n" + sub.to_csv(index=False))

            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":SYSTEM},
                          {"role":"user","content":PROMPT}],
                temperature=0.3, max_tokens=220
            )
            return resp.choices[0].message.content.strip()

        window = st.selectbox("Report window (days)", [7, 14, 30], index=0)
        recent = df.sort_values("date").tail(window)
        st.markdown(ai_report(recent))

        # ---------- lesson card ----------
        st.markdown("---")
        st.subheader("Lesson: Turning words into numbers (data modeling)")
        st.write(
            "Not everyone has instruments. In LearnLab, we map words to numbers so we can graph them. "
            "Example: ‘Cold’ → 15°C, ‘Heavy rain’ → 10 mm, ‘Smoky’ air → PM2.5 of 80. "
            "Using the same scale every day makes patterns easier to see."
        )

# ---------- footer ----------
st.caption("LearnLab is for education. Be safe and respectful collecting data.")