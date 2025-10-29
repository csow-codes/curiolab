import streamlit as st, json, os, random, base64
from theme import apply_global_theme

st.set_page_config(page_title="Get Started", page_icon="🔬", layout="wide")
apply_global_theme()

def cute_box(text: str, bg="#e0f2fe"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

# --- Enhanced CurioLab styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');
html, body, [class^="css"], p, li, span, div { 
  font-family: 'Poppins', system-ui, sans-serif; 
  font-weight: 300;
  color: #a4a4a4;
}
h1, h2, h3, h4, .hero h1, .hero h3 { 
  font-family: 'Nunito', system-ui, sans-serif; 
  font-weight: 900;
  color: #7c9aa8;
}
.hero{
  background:linear-gradient(135deg,#e0f2fe 0%,#ede9fe 50%,#fae8ff 100%);
  border-radius:28px;
  padding:42px 54px;
  margin-bottom:28px;
  text-align:center;
  box-shadow:0 8px 24px rgba(139,92,246,.15);
  border:2px solid #ddd6fe;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '✨🔬🧪⚗️🌱';
  position: absolute;
  top: 20px;
  left: 0;
  width: 100%;
  font-size: 20px;
  opacity: 0.1;
  animation: sparkle 15s linear infinite;
  pointer-events: none;
}
@keyframes sparkle {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
.hero h1{font-size:2.6rem;margin:0 0 8px}
.hero p{color:#a4a4a4;margin:6px 0 0 0;font-weight:300}
.logo-curio{animation:bounce 2s ease-in-out infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}

/* Profile card preview */
.profile-preview {
  background: linear-gradient(135deg, #f0f9ff 0%, #fef3c7 100%);
  border-radius: 20px;
  padding: 24px;
  border: 2px solid #e0e7ff;
  box-shadow: 0 4px 16px rgba(139,92,246,.12);
  margin: 20px 0;
  animation: slideIn 0.5s ease;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Interactive badge */
.badge-preview {
  background: white;
  padding: 16px;
  border-radius: 16px;
  border: 2px solid #e0e7ff;
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.badge-preview::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(167,139,250,0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  border-radius: 50%;
}
.badge-preview:hover::before {
  width: 300px;
  height: 300px;
}
.badge-preview:hover {
  transform: translateY(-5px) scale(1.05) rotate(2deg);
  box-shadow: 0 8px 20px rgba(139,92,246,.3);
}

/* Confetti effect */
@keyframes confetti {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(500px) rotate(360deg); opacity: 0; }
}

/* Shake animation for tips */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Glow effect */
.glow {
  animation: glow 2s ease-in-out infinite;
}
@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px rgba(167,139,250,0.5); }
  50% { box-shadow: 0 0 20px rgba(167,139,250,0.8), 0 0 30px rgba(167,139,250,0.6); }
}

/* Achievement popup */
.achievement-unlock {
  position: fixed;
  top: 80px;
  right: 20px;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.4);
  animation: slideInRight 0.5s ease, pulse 1s ease infinite;
  z-index: 9999;
}
@keyframes slideInRight {
  from { transform: translateX(400px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

/* Mini quiz styling */
.quiz-option {
  background: white;
  padding: 16px;
  border-radius: 12px;
  border: 2px solid #e0e7ff;
  margin: 8px 0;
  cursor: pointer;
  transition: all 0.3s;
}
.quiz-option:hover {
  border-color: #a78bfa;
  transform: translateX(5px);
  box-shadow: 0 2px 12px rgba(167,139,250,.2);
}
.quiz-option.correct {
  background: linear-gradient(135deg, #ecfccb 0%, #fef3c7 100%);
  border-color: #a3e635;
}
.quiz-option.wrong {
  background: #fee;
  border-color: #fca5a5;
}

/* Avatar selector */
.avatar-option {
  font-size: 3rem;
  padding: 16px;
  border-radius: 16px;
  border: 3px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-block;
  margin: 8px;
}
.avatar-option:hover {
  transform: scale(1.2) rotate(10deg);
  border-color: #a78bfa;
  background: #faf5ff;
}
.avatar-option.selected {
  border-color: #7c3aed;
  background: linear-gradient(135deg, #ede9fe 0%, #fae8ff 100%);
  box-shadow: 0 4px 16px rgba(124,58,237,0.3);
}

/* Progress tracker */
.progress-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin: 8px 0;
  border-radius: 12px;
  background: white;
  border: 1px solid #e0e7ff;
  transition: all 0.3s;
}
.progress-step:hover {
  border-color: #a78bfa;
  box-shadow: 0 2px 12px rgba(167,139,250,.15);
}
.progress-step.completed {
  background: linear-gradient(135deg, #ecfccb 0%, #fef3c7 100%);
  border-color: #a3e635;
}
</style>
""", unsafe_allow_html=True)

# --- CurioLab Hero (SINGLE header, no duplicate) ---
logo_path = "avatars/curio_logo.png"
if os.path.exists(logo_path):
    _b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(f"""
    <div class='hero'>
      <div style='display:flex;align-items:center;justify-content:center;gap:16px;position:relative;z-index:1;'>
        <img class='logo-curio' src='data:image/png;base64,{_b64}' style='width:76px;height:76px;border-radius:14px;'>
        <h1>welcome to curiolab</h1>
        <span style='font-size:2.2rem'>🔬</span>
      </div>
      <p>Meet <strong>Dr. Curio</strong>, your capybara mascot. Let's build your scientist profile!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='hero'>
      <div style='display:flex;align-items:center;justify-content:center;gap:16px;position:relative;z-index:1;'>
        <span class='logo-curio' style='font-size:3rem'>🦫</span>
        <h1>welcome to curiolab</h1>
        <span style='font-size:2.2rem'>🔬</span>
      </div>
      <p>Meet <strong>Dr. Curio</strong>, your capybara mascot. Let's build your scientist profile!</p>
    </div>
    """, unsafe_allow_html=True)

def generate_scientist_emoji(name):
    """Generate a unique emoji for each scientist based on their name"""
    emojis = ["🧪", "🔬", "🌱", "🌤️", "🐝", "🔭", "⚗️", "🌍", "🧬", "🔍"]
    random.seed(name)
    return random.choice(emojis)

prof = {}
if os.path.exists("profile.json"):
    try: prof = json.load(open("profile.json","r"))
    except Exception: prof = {}

# Track setup progress
setup_progress = 0
if prof.get("name") and prof["name"] != "Alex": setup_progress += 1
if prof.get("topics"): setup_progress += 1
if prof.get("bio"): setup_progress += 1

# Progress indicator
if setup_progress < 3:
    st.markdown(f"### 🎯 Setup Progress: {setup_progress}/3 Complete")
    st.progress(setup_progress / 3)
    st.caption("Complete all steps to unlock your first badge! ✨")
else:
    st.success("✅ Profile Complete! You're ready to start your science journey!")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 📝 Step 1 — Create Your Scientist Profile")
cute_box("Your profile saves locally. Pick a name, interests, and language. ✨", bg="#e0f2fe")

left, right = st.columns([1,1.2], gap="large")

with left:
    # Avatar selector
    st.markdown("#### 🎨 Choose Your Avatar")
    avatar_emojis = ["🧪", "🔬", "🌱", "🌤️", "🐝", "🔭", "⚗️", "🌍", "🧬", "🔍"]
    
    cols_avatars = st.columns(5)
    selected_avatar = prof.get("avatar", "🔬")
    
    for idx, emoji in enumerate(avatar_emojis):
        with cols_avatars[idx % 5]:
            if st.button(emoji, key=f"avatar_{emoji}", use_container_width=True):
                selected_avatar = emoji
                st.session_state.selected_avatar = emoji
    
    if 'selected_avatar' in st.session_state:
        selected_avatar = st.session_state.selected_avatar
    
    st.markdown(f"<div style='text-align:center;font-size:4rem;margin:16px 0;'>{selected_avatar}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    name = st.text_input("Your name or nickname", value=prof.get("name", "Alex"), help="Shown on your CurioLab cards")

    # --- Safe age selectbox ---
    AGE_CHOICES = ["8–10", "11–13", "14–16"]
    saved_age = prof.get("age")
    if saved_age not in AGE_CHOICES:
        age_index = 1  # default to "11–13"
    else:
        age_index = AGE_CHOICES.index(saved_age)
    age = st.selectbox("Age range", AGE_CHOICES, index=age_index)

    # --- Topics ---
    topics = st.multiselect(
        "Favorite topics",
        ["Environment", "Plants", "Weather", "Health", "Physics", "Space"],
        default=prof.get("topics", ["Environment"])
    )

    # --- Safe language selectbox ---
    LANG_CHOICES = ["English", "Español", "简体中文"]
    saved_lang = prof.get("language", "English")
    lang_index = LANG_CHOICES.index(saved_lang) if saved_lang in LANG_CHOICES else 0
    language = st.selectbox("Language", LANG_CHOICES, index=lang_index)

    st.markdown("---")
    st.markdown("#### 💭 About You")
    bio = st.text_area("What makes you curious? (Optional)", placeholder="E.g., I love watching plants grow or learning about weather! 🌱", height=80, value=prof.get("bio", ""))

    # Show live profile preview
    if name and name != "Alex":
        st.markdown("---")
        st.markdown("#### 👀 Your Profile Preview")
        st.markdown(f"""
        <div class='profile-preview'>
          <div style='display:flex;align-items:center;gap:16px;'>
            <div style='font-size:3rem;'>{selected_avatar}</div>
            <div>
              <h3 style='margin:0;'>{name}</h3>
              <p style='margin:4px 0;font-size:0.9rem;'>Age: {age}</p>
              <p style='margin:4px 0;font-size:0.9rem;'>Interests: {', '.join(topics) if topics else 'None yet'}</p>
            </div>
          </div>
          {f"<p style='margin:12px 0 0 0;font-style:italic;'>'{bio}'</p>" if bio else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🎖️ Starter Badges Preview")
    st.caption("Hover to see what you'll unlock!")
    b1,b2,b3 = st.columns(3)
    with b1: st.markdown("<div class='badge-preview' style='background:#ecfccb;border-color:#a3e635;'>🌱<br><strong>Seedling Scientist</strong></div>", unsafe_allow_html=True)
    with b2: st.markdown("<div class='badge-preview' style='background:#e0f2fe;border-color:#93c5fd;'>🌤️<br><strong>Weather Watcher</strong></div>", unsafe_allow_html=True)
    with b3: st.markdown("<div class='badge-preview' style='background:#fef3c7;border-color:#fbbf24;'>🐝<br><strong>Pollinator Pal</strong></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Save profile button
    if st.button("✨ Save My Profile", type="primary", use_container_width=True):
        badges = []
        if name and name != "Alex":
            badges.append("🌟 Profile Creator")
        
        prof_new = {
            "name": name, "age": age, "topics": topics, "language": language,
            "avatar": selected_avatar,
            "bio": bio,
            "xp": prof.get("xp", 0) + 10,  # Bonus XP for setting up!
            "streak_days": prof.get("streak_days", 0),
            "last_log_date": prof.get("last_log_date", None),
            "badges": badges,
            "experiments_completed": prof.get("experiments_completed", 0)
        }
        json.dump(prof_new, open("profile.json","w"))
        st.success(f"Welcome to CurioLab, {name}! 🎉 You earned 10 XP!")
        st.balloons()
        
        # Show achievement
        st.markdown("""
        <div class='achievement-unlock'>
          <div style='text-align:center;'>
            <div style='font-size:3rem;'>🏆</div>
            <h3 style='margin:8px 0;color:#8b6914;'>Achievement Unlocked!</h3>
            <p style='margin:0;color:#8b6914;font-weight:600;'>Profile Creator</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("### 🧪 Step 2 — How CurioLab Works")
    cute_box("1) Observe → 2) Log data → 3) See charts → 4) Get a Mini Science Report → 5) Share a Science Card", bg="#ecfccb")
    
    # Interactive steps tracker
    st.markdown("#### 📋 Your Research Journey")
    steps = [
        ("🔍 Choose a Mission", "Pick Air Quality, Plant Growth, or Pollinators"),
        ("📝 Log Your Data", "Record observations daily or weekly"),
        ("📊 Watch Patterns Emerge", "See your data visualized in charts"),
        ("🤖 Get AI Insights", "Dr. Curio analyzes your findings"),
        ("🎨 Share Your Discovery", "Create a science card to share")
    ]
    
    for i, (title, desc) in enumerate(steps):
        completed = "completed" if i == 0 else ""
        st.markdown(f"""
        <div class='progress-step {completed}'>
          <div style='font-size:1.5rem;'>{i+1}</div>
          <div>
            <strong>{title}</strong><br>
            <span style='font-size:0.85rem;color:#6b7c8a;'>{desc}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 💬 Dr. Curio's Tip")
    tips = [
        "🕐 Measure at the same time each day for smoother trends!",
        "📝 Add notes about weather or sunlight—context makes your science stronger!",
        "🧪 Try a mini experiment: change one thing and watch the effect!",
        "🔬 The best scientists are curious about everything!",
        "🌟 Consistency beats perfection—just keep observing!",
    ]
    st.info(random.choice(tips))

    # Fun science fact
    st.markdown("#### 🎓 Quick Science Fact")
    facts = [
        "🌱 Plants can communicate underground through fungal networks called 'the Wood Wide Web'!",
        "🐝 A honeybee visits about 5,000 flowers to make one tablespoon of honey!",
        "🌡️ The hottest temperature ever recorded on Earth was 134°F in Death Valley!",
        "☁️ Clouds can weigh over a million pounds even though they float!",
    ]
    st.markdown(f"<div style='background:#fef3c7;padding:16px;border-radius:12px;border:1px solid #fbbf24;'>{random.choice(facts)}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🚀 Step 3 — Jump In")
    st.caption("Choose your first mission!")
    c1,c2,c3 = st.columns(3)
    with c1: 
        st.markdown("<div class='badge-preview'>🌤️<br><strong>Air & Weather</strong></div>", unsafe_allow_html=True)
        st.page_link("pages/2_Air_Quality.py", label="Start Mission →", icon="🌤️")
    with c2: 
        st.markdown("<div class='badge-preview'>🌱<br><strong>Seeds & Growth</strong></div>", unsafe_allow_html=True)
        st.page_link("pages/3_Seeds_Growth.py", label="Start Mission →", icon="🌱")
    with c3: 
        st.markdown("<div class='badge-preview'>🐝<br><strong>Pollinator Patrol</strong></div>", unsafe_allow_html=True)
        st.page_link("pages/4_Pollinator_Patrol.py", label="Start Mission →", icon="🐝")
    
    # Mini quiz game
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎮 Quick Science Quiz")
    st.caption("Test your knowledge while you're here!")
    
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = False
        st.session_state.quiz_correct = False
    
    quiz_questions = [
        {
            "q": "What gives plants their green color?",
            "options": ["Chlorophyll", "Water", "Sunlight", "Carbon dioxide"],
            "correct": 0,
            "explanation": "Chlorophyll is the green pigment that helps plants make food through photosynthesis! 🌱"
        },
        {
            "q": "How long does it take for light from the Sun to reach Earth?",
            "options": ["8 seconds", "8 minutes", "8 hours", "8 days"],
            "correct": 1,
            "explanation": "Light travels at 186,000 miles per second and takes about 8 minutes to reach Earth! ☀️"
        },
        {
            "q": "What percentage of Earth's surface is covered by water?",
            "options": ["50%", "60%", "71%", "85%"],
            "correct": 2,
            "explanation": "About 71% of Earth's surface is covered by water—that's why it's called the Blue Planet! 🌊"
        },
        {
            "q": "How many hearts does an octopus have?",
            "options": ["1", "2", "3", "4"],
            "correct": 2,
            "explanation": "An octopus has three hearts! Two pump blood to the gills, and one pumps it to the rest of the body. 🐙"
        }
    ]
    
    random.seed(prof.get("name", "Alex"))
    current_quiz = random.choice(quiz_questions)
    
    st.markdown(f"**{current_quiz['q']}**")
    
    for idx, option in enumerate(current_quiz['options']):
        if st.button(option, key=f"quiz_{idx}", use_container_width=True):
            st.session_state.quiz_answered = True
            st.session_state.quiz_correct = (idx == current_quiz['correct'])
            st.rerun()
    
    if st.session_state.quiz_answered:
        if st.session_state.quiz_correct:
            st.success(f"🎉 Correct! {current_quiz['explanation']}")
            st.balloons()
        else:
            st.error(f"Not quite! {current_quiz['explanation']}")
        
        if st.button("🔄 Try Another Question"):
            st.session_state.quiz_answered = False
            st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)

# Personality test
st.markdown("### 🧠 What Kind of Scientist Are You?")
st.caption("Take this fun quiz to discover your scientist personality!")

with st.expander("🎯 Take the Personality Quiz"):
    q1 = st.radio(
        "You're outside. What catches your attention first?",
        ["The clouds and weather patterns ☁️", "Plants and insects 🌱", "Rocks and soil 🪨", "Birds and animals 🐦"],
        key="personality_q1"
    )
    
    q2 = st.radio(
        "Your ideal way to spend an afternoon:",
        ["Reading science books 📚", "Doing hands-on experiments 🧪", "Exploring nature 🌲", "Building or creating things 🛠️"],
        key="personality_q2"
    )
    
    q3 = st.radio(
        "When you learn something new, you:",
        ["Write it down carefully 📝", "Try it out immediately 🚀", "Tell everyone about it 🗣️", "Think about how it works 💭"],
        key="personality_q3"
    )
    
    if st.button("🔍 Discover My Scientist Type"):
        # Simple personality mapping
        results = {
            "Meteorologist 🌤️": "You love weather patterns and atmospheric science! Perfect for the Air & Weather mission.",
            "Botanist 🌱": "Plants fascinate you! You'd be amazing at the Seeds & Growth mission.",
            "Ecologist 🐝": "You care about ecosystems and biodiversity. Try the Pollinator Patrol mission!",
            "Experimental Scientist 🧪": "You love trying things out! All missions will be exciting for you."
        }
        
        # Pick based on first answer (simple logic)
        if "clouds" in q1.lower():
            result = "Meteorologist 🌤️"
        elif "plants" in q1.lower() or "insects" in q1.lower():
            result = "Ecologist 🐝"
        elif "rocks" in q1.lower():
            result = "Geologist 🪨"
        else:
            result = "Experimental Scientist 🧪"
        
        st.success(f"**You're a {result}!**")
        st.info(results.get(result, "You're curious about everything! That's the best kind of scientist. 🌟"))
        st.balloons()

st.markdown("<br>", unsafe_allow_html=True)

# Goal setter
st.markdown("### 🎯 Set Your Science Goals")
col_goal1, col_goal2 = st.columns(2)

with col_goal1:
    st.markdown("**This Week:**")
    weekly_goal = st.selectbox(
        "What's your goal?",
        ["Log data 3 times", "Complete 1 mission", "Earn 2 badges", "Learn 5 new facts"],
        key="weekly_goal"
    )
    
with col_goal2:
    st.markdown("**This Month:**")
    monthly_goal = st.selectbox(
        "What's your bigger goal?",
        ["Complete all 3 missions", "Build a 7-day streak", "Earn all starter badges", "Share 3 science cards"],
        key="monthly_goal"
    )

if st.button("💪 Set My Goals", key="set_goals"):
    goals = {
        "weekly": weekly_goal,
        "monthly": monthly_goal
    }
    # Save to profile
    if os.path.exists("profile.json"):
        prof = json.load(open("profile.json", "r"))
        prof["goals"] = goals
        json.dump(prof, open("profile.json", "w"))
    st.success("Goals set! We'll remind you to check your progress. 🎯")

st.markdown("---")
st.caption("🎯 Pro tip: Complete your profile to unlock bonus features!")

