import os, datetime as dt, json, base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from theme import apply_global_theme, header_with_mascot
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Air & Weather", page_icon="🌤️", layout="wide")
apply_global_theme()
header_with_mascot("Air & Weather Lab", "Track temperature, rainfall, and PM2.5 with Dr. Curio")
apply_global_theme()

# Super cute styling
st.markdown("""
<style>
.hero { padding: 40px 50px; }
</style>
""", unsafe_allow_html=True)

def cute_box(text: str, bg="#f8f4ff", emoji="✨"):
    st.markdown(f"""
    <div style='background:{bg};padding:18px 24px;border-radius:20px;border:2px solid #7dd3fc;line-height:1.7;box-shadow:0 3px 10px rgba(125,211,252,0.2);font-size:1.05rem;'>
        <span style='font-size:1.4rem;'>{emoji}</span> {text} <span style='font-size:1.4rem;'>✨</span>
    </div>
    """, unsafe_allow_html=True)

def info_card(title, content, color="#e0f2fe"):
    st.markdown(f"""
    <div style='background:{color};padding:20px;border-radius:16px;border-left:4px solid #0ea5e9;margin:12px 0;'>
        <h4 style='color:#075985;margin-top:0;'>{title}</h4>
        <p style='color:#374151;margin-bottom:0;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

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

def create_beautiful_chart(df, metric, color="#0ea5e9", emoji="🌤️"):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#f0f9ff')
    
    ax.plot(pd.to_datetime(df["date"]), df[metric], marker="o", linewidth=3, 
            markersize=11, color=color, markerfacecolor='#e0f2fe', 
            markeredgewidth=2.5, markeredgecolor=color)
    ax.fill_between(pd.to_datetime(df["date"]), 0, df[metric], 
                    alpha=0.3, color=color)
    
    titles = {"temperature_c": ("🌡️ Temperature Over Time 🌡️", "°C"),
              "rainfall_mm": ("🌧️ Rainfall Over Time 🌧️", "mm"),
              "air_quality_pm": ("💨 Air Quality (PM2.5) Over Time 💨", "µg/m³")}
    
    title, unit = titles.get(metric, (f"{emoji} {metric}", ""))
    ax.set_title(title, fontsize=16, color='#0c4a6e', pad=20, weight='bold')
    ax.set_xlabel("📅 Date", fontsize=13, color='#0ea5e9', weight='bold')
    ax.set_ylabel(f"📊 {unit}", fontsize=13, color='#0ea5e9', weight='bold')
    ax.grid(True, alpha=0.4, linestyle='--', color='#7dd3fc', linewidth=1.5)
    ax.set_facecolor('#f0f9ff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#7dd3fc')
    ax.spines['bottom'].set_color('#7dd3fc')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Header with mascot in hero
header_with_mascot("🌤️ Air & Weather Lab", "Join Dr. Curio to track air and weather!", mascot_path="assets/dr_curio.png", size_px=84)

# Quick Tip
cute_box("💡 Pro Tip: Note clouds, wind, and smells to understand local air quality! Use the kid-friendly choices or advanced numbers for exact measurements!", bg="#e0f2fe", emoji="🌟")

# Educational fun facts
st.markdown("### 🧪 Weather & Air Quality Facts")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("🌡️ Temperature Science", "Temperature affects air density! Warm air rises (that's why balloons go up!), cold air sinks!", "#e0f2fe")
with c2:
    info_card("💨 PM2.5 Explained", "PM2.5 are tiny particles 30x smaller than a hair! They can enter our lungs, so we track them!", "#f0f9ff")
with c3:
    info_card("🌧️ Rainfall Patterns", "Rain helps clean the air by washing particles away! But too much rain means watching for flooding!", "#ecfccb")

st.markdown("---")

# Main input section
st.markdown("### 📝 Your Weather Journal")
left, right = st.columns([1.2, 2], gap="large")

with left:
    st.markdown("#### ✍️ Add New Observation")
    date = st.date_input("📅 Date", value=dt.date.today())
    location = st.text_input("📍 Location", value="My place")
    temp_choice = st.selectbox("🌡️ Temperature (feels like)", ["Cold 🧊","Mild 🙂","Warm 🌤️","Hot 🔥"])
    temp_map = {"Cold 🧊":15,"Mild 🙂":25,"Warm 🌤️":30,"Hot 🔥":35}
    rainfall_choice = st.selectbox("🌧️ Rainfall", ["None ☀️","Light 🌦️","Moderate 🌧️","Heavy ⛈️"])
    rain_map = {"None ☀️":0,"Light 🌦️":2,"Moderate 🌧️":5,"Heavy ⛈️":10}
    air_choice = st.selectbox("💨 Air quality (sky look)", ["Clear 🌈","Hazy 😐","Smoky 😷"])
    air_map = {"Clear 🌈":10,"Hazy 😐":40,"Smoky 😷":80}
    observation = st.text_area("📝 Notes (clouds, wind, smells, etc.)", height=100, 
                                placeholder="E.g., 'Clear sky with wispy clouds, gentle breeze, fresh air!'")

    temperature_c = temp_map[temp_choice]
    rainfall_mm = rain_map[rainfall_choice]
    air_pm = air_map[air_choice]

    with st.expander("🔧 Advanced numbers (optional)"):
        temperature_c = st.number_input("Exact temperature (°C)", value=float(temperature_c), step=0.1)
        rainfall_mm = st.number_input("Exact rainfall (mm)", value=float(rainfall_mm), step=0.1)
        air_pm = st.number_input("Exact PM2.5 (µg/m³)", value=float(air_pm), step=0.1)

    if st.button("✨ Add to Journal", type="primary", use_container_width=True):
        append_row([str(date),location,temperature_c,temp_choice,rainfall_mm,rainfall_choice,air_pm,air_choice,observation])
        add_xp()
        st.success("🌟 Observation saved! +5 XP earned! 🎉")
        st.balloons()

    if os.path.exists(DATA):
        st.download_button("📥 Download Your Data (CSV)", data=open(DATA,"rb").read(), 
                          file_name="air_weather_log.csv", use_container_width=True)

with right:
    df = load_df()
    
    if df.empty:
        cute_box("🌈 Start your weather tracking adventure! Add your first observation on the left to see patterns emerge! 🌈", bg="#e0f2fe", emoji="🌤️")
    else:
        # Weather Stats
        st.markdown("#### 📊 Your Weather Stats")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_temp = df['temperature_c'].mean()
            st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°C")
        with col2:
            total_rain = df['rainfall_mm'].sum()
            st.metric("🌧️ Total Rainfall", f"{total_rain:.1f}mm")
        with col3:
            avg_pm = df['air_quality_pm'].mean()
            pm_status = "Good 🌈" if avg_pm < 30 else "Moderate 😐" if avg_pm < 60 else "Unhealthy 😷"
            st.metric("💨 Avg Air Quality", pm_status)
        with col4:
            st.metric("📅 Observation Days", f"{len(df)}")
        
        # Data-quality nudge
        if len(df) >= 2:
            tmp = df.sort_values("date")
            if abs(tmp["temperature_c"].iloc[-1] - tmp["temperature_c"].iloc[-2]) > 10:
                cute_box("⚠️ Temperature changed >10°C from last entry. Double-check the measurements! 🔍", bg="#fff7ed", emoji="💡")
        
        # Beautiful charts
        st.markdown("---")
        st.markdown("#### 📈 Weather Trends")
        fig1 = create_beautiful_chart(df, "temperature_c", "#0ea5e9", "🌡️")
        st.pyplot(fig1)
        
        st.markdown("---")
        fig2 = create_beautiful_chart(df, "rainfall_mm", "#06b6d4", "🌧️")
        st.pyplot(fig2)
        
        st.markdown("---")
        fig3 = create_beautiful_chart(df, "air_quality_pm", "#8b5cf6", "💨")
        st.pyplot(fig3)

        # Data table
        st.markdown("---")
        st.markdown("#### 📋 All Your Observations")
        st.dataframe(df[["date", "location", "temperature_c", "rainfall_mm", "air_quality_pm", "observation"]].tail(10), 
                     use_container_width=True, hide_index=True)
        
        # Mini Science Report
        st.markdown("---")
        st.markdown("### 🔬 Your Mini Science Report")
        OPENAI = os.getenv("OPENAI_API_KEY")
        def ai_report(rows: pd.DataFrame) -> str:
            sub = rows[["date","location","temperature_c","rainfall_mm","air_quality_pm","observation"]].copy()
            if not OPENAI:
                return ("**🌟 Your Amazing Weather Journey!**\n\n"
                        "You're tracking the climate! 🌤️\n\n"
                        "**Patterns to Look For:**\n"
                        "- Hot days often have clearer skies\n"
                        "- Rain helps clean the air!\n"
                        "- Location affects air quality\n\n"
                        "**Try Next:** Track temperature at the same time each day for a week! 📊")
            try:
                import openai
                openai.api_key = OPENAI
                SYSTEM="You are a friendly, enthusiastic climate science mentor who loves helping kids understand weather and air quality!"
                PROMPT=("Given [date, location, temperature_c, rainfall_mm, air_quality_pm, observation], "
                        "write a fun summary for kids. Mention 2 patterns about weather and air quality, and 1 simple experiment to try next. "
                        "Keep it under 120 words and exciting! Use emojis. Do not invent data.\n\nDATA:\n"+sub.to_csv(index=False))
                resp=openai.chat.completions.create(model="gpt-4o-mini",
                    messages=[{"role":"system","content":SYSTEM},{"role":"user","content":PROMPT}],
                    temperature=0.4, max_tokens=220)
                return resp.choices[0].message.content.strip()
            except Exception as e:
                return f"🤖 AI unavailable: {e}"
        
        window = st.selectbox("📊 Report window (days)", [7, 14, 30], index=0)
        recent = df.sort_values("date").tail(window)
        txt = ai_report(recent)
        
        cute_box(txt, bg="#ecfccb", emoji="🔬")
        st.text_area("💌 Copy & share your science!", value=txt, height=120)

        # Science Story Card
        if st.button("📜 Create Science Story Card!", use_container_width=True):
            card = Image.new("RGB", (520, 720), "#fffdfc")
            d = ImageDraw.Draw(card)
            
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 32)
                body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 18)
            except:
                title_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
            
            d.text((40, 40), "🌤️ Air & Weather — Science Card", fill="#0ea5e9", font=title_font)
            
            body = (txt[:600] + "...") if len(txt) > 600 else txt
            words = body.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + " " + word) < 55:
                    current_line += " " + word if current_line else word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            y = 120
            for line in lines:
                d.text((40, y), line[:60], fill="#374151", font=body_font)
                y += 35
            
            out = "assets/cards/air_story_card.png"
            card.save(out)
            st.image(out, width=400)
            st.download_button("📥 Download Your Science Card!", 
                              data=open(out, "rb").read(), 
                              file_name="Air_Story_Card.png")

# Educational section
st.markdown("---")
st.markdown("### 🌿 Fun Learning Zone")

tab1, tab2, tab3 = st.tabs(["🌡️ Temperature Science", "💨 Air Quality Explained", "🌧️ Weather Patterns"])
with tab1:
    st.markdown("""
    <div style='padding:20px;background:#e0f2fe;border-radius:16px;'>
        <h3>🌡️ The Science of Temperature</h3>
        <p><strong>🌡️ What is Temperature?</strong><br>
        Temperature measures how hot or cold something is. It affects everything around us!</p>
        <p><strong>🔥 Hot Air Rises:</strong> Warm air is lighter and rises into the sky. That's why hot air balloons work!</p>
        <p><strong>❄️ Cold Air Sinks:</strong> Cold air is heavier and sinks down. That's why valleys get colder!</p>
        <p><strong>☀️ Sun Power:</strong> The sun heats the earth's surface. Different places get different amounts of sunlight!</p>
        <p><strong>🌍 Layers of Air:</strong> The atmosphere has layers with different temperatures. Space is very cold, but near volcanoes it's hot!</p>
        <p><strong>📊 Why Track It:</strong> Temperature affects our health, plants, animals, and even how much energy we need!</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style='padding:20px;background:#f0f9ff;border-radius:16px;'>
        <h3>💨 Air Quality & PM2.5</h3>
        <p><strong>💨 What is PM2.5?</strong><br>
        PM2.5 are tiny particles 30x smaller than a human hair! They float in the air we breathe.</p>
        <p><strong>😷 Where They Come From:</strong> Cars, factories, fires, and even nature (pollen, dust). Some sources are natural, some are from human activity.</p>
        <p><strong>❤️ Why It Matters:</strong> These tiny particles can get deep into our lungs and affect our health. Clean air is important!</p>
        <p><strong>🌈 Clear Air:</strong> PM2.5 below 30 µg/m³ is considered good quality air!</p>
        <p><strong>🌿 Nature Helps:</strong> Trees and plants filter air naturally! They're nature's air purifiers!</p>
        <p><strong>📈 Your Role:</strong> By tracking air quality, you're helping scientists understand local pollution patterns!</p>
        <p><strong>🌬️ Wind Helps:</strong> Wind can blow pollution away and bring fresh air from other places!</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div style='padding:20px;background:#ecfccb;border-radius:16px;'>
        <h3>🌧️ Weather Patterns & Climate</h3>
        <p><strong>🌧️ Why Does It Rain?</strong><br>
        When water evaporates from lakes and oceans, it rises and cools, forming clouds. When clouds get heavy, rain falls!</p>
        <p><strong>☁️ Types of Clouds:</strong> Different clouds mean different weather! Cumulus = fluffy fair weather, Stratus = gray rain clouds!</p>
        <p><strong>🌬️ Wind Patterns:</strong> Wind is caused by differences in air pressure. Warm and cold air meet and create movement!</p>
        <p><strong>🌍 Local Weather:</strong> Your local area (mountains, oceans, cities) affects your weather patterns!</p>
        <p><strong>📅 Seasons:</strong> Weather changes with seasons because Earth tilts as it orbits the sun!</p>
        <p><strong>🔍 Your Data:</strong> By tracking weather over time, you can predict patterns and understand your local climate!</p>
    </div>
    """, unsafe_allow_html=True)