import os, datetime as dt, json, base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from theme import apply_global_theme, header_with_mascot
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Pollinator Patrol", page_icon="🐝", layout="wide")
apply_global_theme()

# Super cute styling
st.markdown("""
<style>
.hero { padding: 40px 50px; }
</style>
""", unsafe_allow_html=True)

# Header
header_with_mascot("Pollinator Patrol", "Count pollinators with Dr. Curio!", mascot_path="assets/dr_curio.png", size_px=84)

def cute_box(text: str, bg="#f8f4ff", emoji="✨"):
    st.markdown(f"""
    <div style='background:{bg};padding:18px 24px;border-radius:20px;border:2px solid #fbbf24;line-height:1.7;box-shadow:0 3px 10px rgba(252,165,165,0.2);font-size:1.05rem;'>
        <span style='font-size:1.4rem;'>{emoji}</span> {text} <span style='font-size:1.4rem;'>✨</span>
    </div>
    """, unsafe_allow_html=True)

def info_card(title, content, color="#fef3c7"):
    st.markdown(f"""
    <div style='background:{color};padding:20px;border-radius:16px;border-left:4px solid #f59e0b;margin:12px 0;'>
        <h4 style='color:#92400e;margin-top:0;'>{title}</h4>
        <p style='color:#374151;margin-bottom:0;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

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

def create_beautiful_chart(df, species="bees"):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#fffbf0')
    color = '#f59e0b' if species == "bees" else '#ec4899'
    
    ax.plot(pd.to_datetime(df["date"]), df[species], marker="o", linewidth=3, 
            markersize=11, color=color, markerfacecolor='#fef3c7', 
            markeredgewidth=2.5, markeredgecolor=color)
    ax.fill_between(pd.to_datetime(df["date"]), 0, df[species], 
                    alpha=0.3, color=color)
    
    emoji = "🐝" if species == "bees" else "🦋"
    ax.set_title(f"{emoji} {species.capitalize()} Visits Over Time {emoji}", 
                fontsize=16, color='#92400e', pad=20, weight='bold')
    ax.set_xlabel("📅 Date", fontsize=13, color='#f59e0b', weight='bold')
    ax.set_ylabel("👥 Count (10 min)", fontsize=13, color='#f59e0b', weight='bold')
    ax.grid(True, alpha=0.4, linestyle='--', color='#fbbf24', linewidth=1.5)
    ax.set_facecolor('#fffbf0')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#fbbf24')
    ax.spines['bottom'].set_color('#fbbf24')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Quick Tip
cute_box("💡 Pro Tip: Watch for 10 minutes and count from a safe distance. Note the weather ☀️ and flower blooms 🌸 to understand what attracts pollinators!", bg="#fef3c7", emoji="🌟")

# Educational fun facts
st.markdown("### 🧪 Pollinator Power Facts")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("🐝 Why Bees Matter", "Bees pollinate 1 in 3 bites of food! Without them, many fruits and vegetables would disappear!", "#fef3c7")
with c2:
    info_card("🦋 Butterfly Magic", "Butterflies are like flying flowers! They pollinate while searching for nectar, helping gardens bloom!", "#fce7f3")
with c3:
    info_card("🌸 Biodiversity Bonus", "More pollinators = more flowers = healthier ecosystems! You're making a difference!", "#e0f2fe")

st.markdown("---")

# Main input section
st.markdown("### 📝 Your Pollinator Journal")
left, right = st.columns([1.2, 2], gap="large")

with left:
    st.markdown("#### ✍️ Add New Observation")
    date = st.date_input("📅 Date", value=dt.date.today())
    location = st.text_input("📍 Location", value="School garden")
    bees = st.slider("🐝 Bees spotted (10 min)", 0, 50, 3)
    butterflies = st.slider("🦋 Butterflies spotted (10 min)", 0, 30, 1)
    flowers = st.selectbox("🌸 Flower Bloom Level", ["None 🌿", "Some 🌸", "Lots 🌺"])
    weather = st.selectbox("🌤️ Weather", ["Sunny ☀️", "Cloudy ☁️", "Windy 🍃", "Rainy 🌧️"])
    notes = st.text_area("📝 Notes (species, behavior, time, etc.)", height=100, 
                         placeholder="E.g., 'Honeybees on lavender, monarch butterfly near rose, sunny afternoon!'")
    
    if st.button("✨ Add to Patrol", type="primary", use_container_width=True):
        append_row([str(date), location, bees, butterflies, flowers, weather, notes])
        add_xp()
        st.success("🌟 Observation saved! +5 XP earned! 🎉")
        st.balloons()
    
    if os.path.exists(DATA):
        st.download_button("📥 Download Your Data (CSV)", data=open(DATA,"rb").read(), 
                          file_name="pollinator_patrol_log.csv", use_container_width=True)

with right:
    df = load_df()
    
    if df.empty:
        cute_box("🌈 Start your pollinator adventure! Add your first observation on the left to track biodiversity! 🌈", bg="#e0f2fe", emoji="🐝")
    else:
        # Biodiversity Stats
        st.markdown("#### 📊 Your Biodiversity Stats")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🐝 Total Bees Spotted", f"{df['bees'].sum()}")
        with col2:
            st.metric("🦋 Total Butterflies", f"{df['butterflies'].sum()}")
        with col3:
            total_pollinators = df['bees'].sum() + df['butterflies'].sum()
            st.metric("🌺 Biodiversity Index", f"{total_pollinators}")
        with col4:
            st.metric("📅 Observation Days", f"{len(df)}")
        
        # Beautiful charts
        st.markdown("#### 📈 Pollinator Activity Trends")
        chart1, chart2 = st.columns(2)
        with chart1:
            fig1 = create_beautiful_chart(df, "bees")
            st.pyplot(fig1)
        with chart2:
            fig2 = create_beautiful_chart(df, "butterflies")
            st.pyplot(fig2)
        
        # Patterns by conditions
        st.markdown("---")
        st.markdown("#### 🔍 Discover Patterns!")
        p1, p2 = st.columns(2)
        
        with p1:
            st.markdown("##### ☀️ Weather Patterns")
            weather_df = df.groupby("weather")[["bees","butterflies"]].mean().round(1)
            weather_df.columns = ["🐝 Bees", "🦋 Butterflies"]
            st.dataframe(weather_df, use_container_width=True)
        
        with p2:
            st.markdown("##### 🌸 Flower Bloom Effect")
            flower_df = df.groupby("flowers")[["bees","butterflies"]].mean().round(1)
            flower_df.columns = ["🐝 Bees", "🦋 Butterflies"]
            st.dataframe(flower_df, use_container_width=True)
        
        # Location stats
        if len(df) > 1:
            st.markdown("##### 📍 Top Observation Locations")
            location_stats = df.groupby("location")[["bees", "butterflies"]].sum().sum(axis=1).sort_values(ascending=False).head(5)
            for loc, count in location_stats.items():
                progress = count / location_stats.max() if location_stats.max() > 0 else 0
                st.markdown(f"**{loc}**: {count} total visitors")
                st.progress(progress)
        
        # Data table
        st.markdown("---")
        st.markdown("#### 📋 All Your Observations")
        st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
        
        # Mini Science Report
        st.markdown("---")
        st.markdown("### 🔬 Your Mini Science Report")
        OPENAI = os.getenv("OPENAI_API_KEY")
        if OPENAI:
            try:
                import openai
                openai.api_key = OPENAI
                prompt = ("You are a friendly science mentor for kids. Summarize this pollinator observation data in a fun, encouraging way. "
                          "Mention 2 interesting patterns about what attracts pollinators and 1 simple experiment they could try next. "
                          "Keep it under 120 words and exciting! Use emojis. Do not invent data that doesn't exist.\n\nDATA:\n" + df.to_csv(index=False))
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":"You are a friendly, enthusiastic biodiversity mentor who loves helping kids discover ecology!"},
                              {"role":"user","content":prompt}],
                    temperature=0.4, max_tokens=220
                )
                txt = resp.choices[0].message.content.strip()
            except Exception as e:
                txt = f"🤖 AI unavailable: {e}"
        else:
            txt = ("**🌟 Your Amazing Biodiversity Journey!**\n\n"
                   "You're discovering the secret world of pollinators! 🐝🦋\n\n"
                   "**Patterns You Might See:**\n"
                   "- Sunny days ☀️ attract more visitors\n"
                   "- More flowers 🌸 = more pollinators\n"
                   "- Location matters - gardens vs parks!\n\n"
                   "**Try Next:** Test which flower colors attract the most visitors! 🌈")
        
        cute_box(txt, bg="#fce7f3", emoji="🔬")
        st.text_area("💌 Copy & share your science!", value=txt, height=120)
        
        # Story card
        if st.button("📜 Create Science Story Card!", use_container_width=True):
            card = Image.new("RGB", (520, 720), "#fffdfc")
            d = ImageDraw.Draw(card)
            
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 32)
                body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 18)
            except:
                title_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
            
            d.text((40, 40), "🐝 Pollinator Patrol — Science Card", fill="#f59e0b", font=title_font)
            
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
            
            out = "assets/cards/pollinator_story_card.png"
            card.save(out)
            st.image(out, width=400)
            st.download_button("📥 Download Your Science Card!", 
                              data=open(out, "rb").read(), 
                              file_name="Pollinator_Story_Card.png")

# Educational section
st.markdown("---")
st.markdown("### 🌿 Fun Learning Zone")

tab1, tab2, tab3 = st.tabs(["🐝 Meet the Pollinators", "🌸 How to Help", "🔬 Pollinator Science"])
with tab1:
    st.markdown("""
    <div style='padding:20px;background:#fef3c7;border-radius:16px;'>
        <h3>🐝 Meet Your Pollinator Friends</h3>
        <p><strong>🐝 Honeybees:</strong> Fuzzy workers who visit flowers to collect nectar and pollen. They live in hives and communicate with dances!</p>
        <p><strong>🦋 Butterflies:</strong> Beautiful flyers who love sunshine! They use their long proboscis (like a straw) to drink nectar from flowers.</p>
        <p><strong>🐝 Bumblebees:</strong> Bigger, fuzzier cousins of honeybees. They can buzz-pollinate by vibrating flowers!</p>
        <p><strong>🐝 Mason Bees:</strong> Solitary bees that nest in tiny holes. Super efficient pollinators!</p>
        <p><strong>🦟 Hoverflies:</strong> Look like bees but have one set of wings. Great pollinators too!</p>
        <p><strong>🌻 The Challenge:</strong> Many pollinators are declining due to habitat loss and pesticides. You're helping track them!</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style='padding:20px;background:#fce7f3;border-radius:16px;'>
        <h3>🌸 How You Can Help Pollinators</h3>
        <p><strong>🌸 Plant Native Flowers:</strong> Local flowers attract local pollinators best!</p>
        <p><strong>❌ Skip Pesticides:</strong> Chemicals hurt the pollinators we need. Use natural pest control instead.</p>
        <p><strong>💧 Provide Water:</strong> A shallow dish with rocks gives pollinators a safe place to drink.</p>
        <p><strong>🏡 Create Habitat:</strong> Leave some wild areas for pollinators to nest and shelter.</p>
        <p><strong>📅 Watch Consistently:</strong> Compare observations at the same time of day for better data.</p>
        <p><strong>📸 Take Pictures:</strong> Photos help you identify species and track individual pollinators!</p>
        <p><strong>🌺 Diversity Matters:</strong> Plant different flowers that bloom all season for year-round support!</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div style='padding:20px;background:#e0f2fe;border-radius:16px;'>
        <h3>🔬 Fun Pollinator Science</h3>
        <p><strong>🌻 Flower Color Science:</strong> Different colors attract different pollinators! Bees love blues and yellows, butterflies prefer red and orange!</p>
        <p><strong>🎵 The Waggle Dance:</strong> Honeybees do a dance to tell other bees where flowers are! It's like GPS for bees!</p>
        <p><strong>🍯 Pollen Collection:</strong> Bees carry pollen in special baskets on their legs. It's how flowers get fertilized!</p>
        <p><strong>🦋 Metamorphosis Magic:</strong> Butterflies go through 4 stages: egg → caterpillar → chrysalis → butterfly! Complete transformation!</p>
        <p><strong>🌺 Nectar Guides:</strong> Many flowers have UV patterns invisible to us but visible to pollinators! It's their own secret map!</p>
        <p><strong>📊 Your Impact:</strong> By observing and documenting pollinators, you're contributing to real science that helps protect biodiversity!</p>
    </div>
    """, unsafe_allow_html=True)
