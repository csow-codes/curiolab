import os, datetime as dt, json, base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from theme import apply_global_theme, header_with_mascot
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Seeds & Growth", page_icon="🔬", layout="wide")
apply_global_theme()

# Super cute styling
st.markdown("""
<style>
.hero { padding: 40px 50px; }
.section {margin: 32px 0; padding: 24px; background: #fff; border-radius: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);}
</style>
""", unsafe_allow_html=True)

# Header
header_with_mascot("CurioLab", "Seeds and Growth: Track plant growth with Dr. Curio!", mascot_path="assets/dr_curio.png", size_px=140)

def cute_box(text: str, bg="#f8f4ff", emoji="✨"):
    st.markdown(f"""
    <div style='background:{bg};padding:18px 24px;border-radius:20px;border:2px solid #d8b4fe;line-height:1.7;box-shadow:0 3px 10px rgba(167,139,250,0.2);font-size:1.05rem;'>
        <span style='font-size:1.4rem;'>{emoji}</span> {text} <span style='font-size:1.4rem;'>✨</span>
    </div>
    """, unsafe_allow_html=True)

def info_card(title, content, color="#e0f2fe"):
    st.markdown(f"""
    <div style='background:{color};padding:20px;border-radius:16px;border-left:4px solid #7c3aed;margin:12px 0;'>
        <h4 style='color:#6b21a8;margin-top:0;'>{title}</h4>
        <p style='color:#374151;margin-bottom:0;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

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

def create_beautiful_chart(df, plant_name):
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='#fef3ff')
    colors = plt.cm.Purples(np.linspace(0.4, 0.9, len(df)))
    
    ax.plot(pd.to_datetime(df["date"]), df["height_cm"], marker="o", linewidth=3, 
            markersize=11, color='#7c3aed', markerfacecolor='#fef3ff', 
            markeredgewidth=2.5, markeredgecolor='#c4b5fd', label='Growth')
    ax.fill_between(pd.to_datetime(df["date"]), 0, df["height_cm"], 
                    alpha=0.25, color='#7c3aed')
    
    ax.set_title(f"🌱 {plant_name}'s Amazing Growth Journey 🌱", 
                fontsize=16, color='#6b21a8', pad=20, weight='bold')
    ax.set_xlabel("📅 Date", fontsize=13, color='#7c3aed', weight='bold')
    ax.set_ylabel("📏 Height (cm)", fontsize=13, color='#7c3aed', weight='bold')
    ax.grid(True, alpha=0.4, linestyle='--', color='#c4b5fd', linewidth=1.5)
    ax.set_facecolor('#fef3ff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#c4b5fd')
    ax.spines['bottom'].set_color('#c4b5fd')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Quick Tip
cute_box("💡 Pro Tip: Measure at the same time each day for the smoothest curves! Add notes about sunlight ☀️, water 💧, and soil 🌍 to explain the growth patterns.", bg="#fef3c7", emoji="🌟")

# Educational fun facts
st.markdown("### 🧪 Quick Science Facts")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("🌍 How Plants Eat", "Plants make their own food using sunlight through photosynthesis! It's like having a solar-powered kitchen in each leaf!", "#ecfccb")
with c2:
    info_card("💧 Why Water Matters", "Water carries nutrients from roots to leaves. Without enough water, plants can't grow or make food properly!", "#e0f2fe")
with c3:
    info_card("🌱 Growing Up", "Plants grow from tiny seeds because of hormones called auxins that tell cells when to divide and grow taller!", "#fce7f3")

st.markdown("---")

# Main input section
st.markdown("### 📝 Your Plant Journal")
left, right = st.columns([1.2, 2], gap="large")

with left:
    st.markdown("#### ✍️ Add New Observation")
    date = st.date_input("📅 Date", value=dt.date.today())
    plant = st.text_input("🌿 Plant Name", value="Bean")
    height = st.number_input("📏 Height (cm)", value=3.0, step=0.1)
    notes = st.text_area("📝 Notes (sunlight ☀️, water 💧, soil, weather, etc.)", height=100, 
                         placeholder="E.g., 'Sunny day ☀️, watered in morning 💧, leaves turning greener!'")
    if st.button("✨ Add to Journal", type="primary", use_container_width=True):
        append_row([str(date),plant,height,notes])
        add_xp()
        st.success("🌟 Added successfully! +5 XP earned! 🎉")
        st.balloons()
    
    if os.path.exists(DATA):
        st.download_button("📥 Download Your Data (CSV)", data=open(DATA,"rb").read(), 
                          file_name="seeds_growth_log.csv", use_container_width=True)

with right:
    df = load_df()
    
    if df.empty:
        cute_box("🌈 Start your plant adventure! Add your first observation on the left to see your plant's growth journey! 🌈", bg="#e0f2fe", emoji="🌱")
    else:
        # Growth Stats
        st.markdown("#### 📊 Your Growth Stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Total Growth", f"+{df['height_cm'].max() - df['height_cm'].min():.1f} cm")
        with col2:
            st.metric("📅 Days Tracked", f"{len(df)} days")
        with col3:
            avg_growth = (df['height_cm'].iloc[-1] - df['height_cm'].iloc[0]) / len(df) if len(df) > 1 else 0
            st.metric("🌿 Avg Daily Growth", f"{avg_growth:.2f} cm/day")
        
        # Beautiful chart
        st.markdown("#### 📈 Growth Visualization")
        plant_name = df["plant"].iloc[0] if not df.empty else "Plant"
        fig = create_beautiful_chart(df, plant_name)
        st.pyplot(fig)
        
        # Data table
        st.markdown("#### 📋 All Your Observations")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Mini Science Report
        st.markdown("---")
        st.markdown("### 🔬 Your Mini Science Report")
        OPENAI = os.getenv("OPENAI_API_KEY")
        if OPENAI:
            try:
                import openai
                openai.api_key = OPENAI
                prompt = ("You are a friendly science mentor for kids. Summarize this plant growth data in a fun, encouraging way. "
                          "Mention 2 interesting patterns you notice and 1 simple experiment they could try next. "
                          "Keep it under 100 words and exciting! Use emojis. Do not invent data that doesn't exist in the data.\n\nDATA:\n" + df.to_csv(index=False))
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":"You are a friendly, enthusiastic science mentor who loves helping kids discover science!"},
                              {"role":"user","content":prompt}],
                    temperature=0.4, max_tokens=180
                )
                txt = resp.choices[0].message.content.strip()
            except Exception as e:
                txt = f"🤖 AI unavailable: {e}"
        else:
            txt = ("**🌟 Your Amazing Plant Journey!**\n\n"
                   "Your plant has been growing steadily! 📈\n\n"
                   "**Patterns:**\n"
                   "- Sunny days ☀️ often show bigger growth\n"
                   "- Consistent watering 💧 helps steady progress\n\n"
                   "**Try Next:** Track sunlight hours each day and compare to growth rate! 🌈")
        
        cute_box(txt, bg="#ecfccb", emoji="🔬")
        st.text_area("💌 Copy & share your science!", value=txt, height=120)
        
        # Story card
        if st.button("📜 Create Science Story Card!", use_container_width=True):
            card = Image.new("RGB", (520, 720), "#fffdfc")
            d = ImageDraw.Draw(card)
            
            # Try to use a nicer font if available
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 32)
                body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 18)
            except:
                title_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
            
            # Title
            d.text((40, 40), "🌱 Seeds & Growth — Science Card", fill="#7c3aed", font=title_font)
            
            # Content
            body = (txt[:600] + "...") if len(txt) > 600 else txt
            # Simple text wrapping
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
            
            out = "assets/cards/seeds_story_card.png"
            card.save(out)
            st.image(out, width=400)
            st.download_button("📥 Download Your Science Card!", 
                              data=open(out, "rb").read(), 
                              file_name="Seeds_Story_Card.png")

# Educational section
st.markdown("---")
st.markdown("### 🌿 Fun Learning Zone")

tab1, tab2, tab3 = st.tabs(["🌱 How Plants Grow", "💧 Plant Care Tips", "🔬 Science Experiments"])
with tab1:
    st.markdown("""
    <div style='padding:20px;background:#f8f4ff;border-radius:16px;'>
        <h3>🌱 The Amazing Journey of a Seed</h3>
        <p><strong>1. Germination 🌾</strong><br>
        A seed needs water, warmth, and oxygen to sprout! The first little root grows downward to find nutrients.</p>
        <p><strong>2. Photosynthesis 🌞</strong><br>
        Green leaves capture sunlight and turn it into food using carbon dioxide from air and water from roots!</p>
        <p><strong>3. Growth 🌿</strong><br>
        Plants have special cells that divide to make them grow taller. They need sunlight, water, and nutrients from soil.</p>
        <p><strong>4. Flowering & Seeds 🌸</strong><br>
        When mature, plants make flowers and seeds to create new plants - it's nature's way of continuing life!</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style='padding:20px;background:#ecfccb;border-radius:16px;'>
        <h3>💧 Plant Care for Young Scientists</h3>
        <p><strong>☀️ Sunlight:</strong> Plants need light to make food! Most need 4-6 hours of sunlight daily.</p>
        <p><strong>💧 Water:</strong> Water regularly but don't overwater! Check soil moisture with your finger.</p>
        <p><strong>🌍 Soil:</strong> Good soil has nutrients and drains well. Plants need air around their roots too!</p>
        <p><strong>📅 Consistency:</strong> Measure at the same time each day for the most accurate data!</p>
        <p><strong>📊 Keep Notes:</strong> Write down what you do - watering, weather, location - to learn what works best!</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div style='padding:20px;background:#e0f2fe;border-radius:16px;'>
        <h3>🔬 Easy Experiments to Try</h3>
        <p><strong>1. Light vs Dark 🌞/🌙</strong><br>
        Grow two identical plants - one in sunlight, one in darkness. Compare after a week!</p>
        <p><strong>2. Water Amounts 💧</strong><br>
        Give different plants different amounts of water daily. Which grows fastest?</p>
        <p><strong>3. Soil Types 🌍</strong><br>
        Try growing the same plant in different soils (sand, clay, potting mix) and see which works best!</p>
        <p><strong>4. Plant Music 🎵</strong><br>
        Some studies suggest music helps plants grow! Try playing music to one plant and compare growth!</p>
        <p><strong>💡 Remember:</strong> Always use the scientific method - form a hypothesis, test it, record results, and draw conclusions!</p>
    </div>
    """, unsafe_allow_html=True)
