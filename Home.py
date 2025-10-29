import streamlit as st, json, os, random, datetime as dt
from lang import t
from theme import apply_global_theme, header_with_mascot

import re
def get_science_buddy_response(question):
    q_lower = question.lower()
    
    # Comprehensive science knowledge base
    responses = {
        # Biology
        "green|chlorophyll|leaf|leaves": "Great question! Plants are green because of chlorophyll, a special pigment in their leaves. Chlorophyll absorbs red and blue light from the sun for photosynthesis, but reflects green light back to our eyes. That's why we see them as green!",
        
        "photosynthesis|food|energy": "Excellent question! Photosynthesis is how plants make their own food! They use sunlight, water from the soil, and carbon dioxide from the air to create glucose (sugar) for energy. As a bonus, they release oxygen that we breathe. Isn't that super cool?",
        
        "root|roots": "Roots are like a plant's underground support system! They anchor the plant in soil, absorb water and nutrients, and even store food. Some roots can sense gravity and water, helping them grow in the right direction. It's super interesting!!",
        
        "flower|pollen|pollination": "Yess, great question!! Flowers are a plant's way of making seeds! They attract pollinators like bees and butterflies with bright colors and sweet nectar. When pollinators visit, they carry pollen from flower to flower, helping plants reproduce.",
        
        # Weather and Atmosphere
        "sky|blue|atmosphere": "Awesome question! The sky is blue because of something called Rayleigh scattering. Sunlight is made of all colors, but blue light has shorter waves that scatter more when hitting air molecules. That scattered blue light reaches our eyes from all directions, making the sky look blue!",
        
        "rain|rainfall|precipitation": "Good thinking! Rain forms when water vapor in clouds condenses into droplets. As the droplets get bigger and heavier, gravity pulls them down to Earth. Temperature, air pressure, and humidity all work together to create rain!",
        
        "cloud|clouds": "Clouds form when water vapor in the air cools down and condenses into tiny water droplets or ice crystals. These droplets are so light they float in the sky! Different cloud shapes tell us about weather patterns, for example, fluffy cumulus clouds usually mean nice weather, while dark nimbus clouds bring rain!",
        
        "thunder|lightning": "Lightning happens when ice particles in clouds bump together, creating static electricity like when you rub a balloon on your hair! When the charge gets strong enough, it jumps as lightning. Thunder is the sound of air rapidly heating and expanding from the lightning's intense heat!",
        
        "rainbow": "Rainbows appear when sunlight shines through water droplets in the air. Each droplet acts like a tiny prism, splitting white light into its seven colors: red, orange, yellow, green, blue, indigo, and violet. The colors always appear in the same order because each color bends at a slightly different angle!",
        
        "wind": " Wind is simply air in motion! It happens because the Sun heats different parts of Earth unevenly. Warm air rises and cool air rushes in to fill the space, creating wind. The greater the temperature difference, the stronger the wind!",
        
        # Astro
        "star|stars|twinkle": "Stars twinkle because their light passes through Earth's atmosphere, which is constantly moving. The moving air bends and bounces the light around, making stars appear to flicker. In space, astronauts see stars that don't twinkle at all!",
        
        "moon|lunar": "The Moon doesn't make its own light - it reflects light from the Sun! We see different moon phases because the Sun lights up different parts of the Moon as it orbits Earth. A full moon happens when the Sun lights up the whole side facing us!",
        
        "sun|solar": "The Sun is a giant ball of hot gas - mostly hydrogen and helium. In its core, hydrogen atoms smash together to form helium in a process called nuclear fusion. This releases enormous amounts of energy as heat and light. The Sun is so big that over a million Earths could fit inside it!",
        
        "planet|planets": "Our solar system has 8 planets orbiting the Sun. The inner four (Mercury, Venus, Earth, Mars) are rocky planets. The outer four (Jupiter, Saturn, Uranus, Neptune) are gas giants. Each planet has unique features - Saturn has beautiful rings, Jupiter has a giant storm called the Great Red Spot!",
        
        "gravity": "Gravity is an invisible force that pulls objects toward each other. The bigger and closer an object is, the stronger its gravitational pull. Earth's gravity keeps us on the ground and the Moon in orbit. Without gravity, we'd float off into space!",
        
        # Animals and Insects
        "bee|bees": "Bees are amazing insects! They can see ultraviolet colors we can't see, recognize human faces, and communicate through special dances. When a bee finds flowers with nectar, it does a 'waggle dance' to tell other bees exactly where to find them. Plus, they're essential pollinators for our food!",
        
        "butterfly|butterflies": "Butterflies taste with their feet! They have taste sensors on their legs that help them know if a plant is good for laying eggs. Their wings are covered in thousands of tiny scales that create their beautiful colors. Some butterflies migrate thousands of miles!",
        
        "bird|birds|fly|flight": "Birds can fly because they have several special features: lightweight hollow bones, powerful flight muscles, and feathers shaped like airfoils (like airplane wings). When they flap their wings, they create lift that pushes them up. Different wing shapes help birds fly in different ways!",
        
        "fish|swim": "Fish breathe underwater using gills! As water flows over their gills, oxygen dissolved in the water passes into their blood, and carbon dioxide passes out. Their streamlined bodies and fins help them move efficiently through water. Some fish can even breathe air or survive in ice-cold waters!",
        
        # Physics and Chem
        "water|h2o": "Water is special! It's made of two hydrogen atoms and one oxygen atom (H₂O). Water is the only substance that naturally exists in all three states on Earth: solid (ice), liquid (water), and gas (steam). It expands when it freezes, which is why ice floats!",
        
        "magnet|magnetic": "Magnets work because of invisible magnetic fields created by moving electrons. Every magnet has two poles: north and south. Opposite poles attract each other, while same poles repel. Earth itself is like a giant magnet, which is why compass needles point north!",
        
        "color|colors": "Colors are actually different wavelengths of light! When light hits an object, some wavelengths are absorbed and others are reflected. We see the reflected wavelengths as color. A red apple absorbs all colors except red, which bounces back to our eyes!",
        
        "sound|hear|noise": "Sound travels in waves through air, water, or solid objects. When something vibrates, it pushes air molecules, creating a wave that travels to your ear. Your eardrum vibrates from these waves, and your brain interprets them as sound. Sound can't travel in space because there's no air!",
        
        "temperature|hot|cold|heat": "Temperature measures how fast molecules are moving! When something is hot, its molecules vibrate quickly. When it's cold, they slow down. Heat always flows from hot to cold objects until they reach the same temperature. That's why metal feels colder than wood - it conducts heat away from your hand faster!",
        
        # Human Body
        "blood|heart": "Your heart is an amazing pump that beats about 100,000 times per day! It pumps blood through your body, delivering oxygen and nutrients to every cell. Blood picks up oxygen in your lungs and carries it everywhere. Red blood cells contain iron, which is why blood is red!",
        
        "brain": "Your brain is like a supercomputer with about 86 billion neurons! It controls everything you do - thinking, moving, feeling, and even things you don't think about like breathing. Different parts handle different jobs: the cerebrum for thinking, cerebellum for balance, and brain stem for automatic functions!",
        
        "breathe|breathing|lung|lungs": "When you breathe in, your lungs fill with air containing oxygen. Tiny air sacs called alveoli transfer oxygen into your blood. Your blood carries oxygen to all your body's cells. When you breathe out, you release carbon dioxide, a waste product cells don't need!",
        
        # General Science
        "experiment|science": "Experiments are how scientists test their ideas! The scientific method involves: 1) Asking a question, 2) Forming a hypothesis (educated guess), 3) Testing it with an experiment, 4) Observing what happens, and 5) Drawing conclusions. Even if your hypothesis is wrong, you still learn something valuable!",
        
        "dna|gene|genetics": "DNA is like your body's instruction manual! It's shaped like a twisted ladder (double helix) and contains all the information needed to build and run your body. You inherit half your DNA from each parent, which is why you might look like them. DNA is in almost every cell of your body!",
    }
    
    # Try to match patterns in the question
    for pattern, response in responses.items():
        if re.search(pattern, q_lower):
            return response
    
    # Encouraging responses for questions we don't have specific answers for
    encouragement_responses = [
        "That's a really cool question! Try searching for it online, asking your teacher or parents, or even doing a simple experiment to find out! Curiosity and discovery is what science is all about.",
        
        "What a great question! That's exactly the kind of questions that scientists ask! You might want to investigate this through observation, research, or designing an experiment. What do you personally think might be the answer?",
        
        "That's a question worth exploring! You might find answers by reading science books, watching educational videos, or talking with scientists. Sometimes the best way to learn is to investigate yourself!",
        
        "Wow, what an fun question! I encourage you to research this topic, because you might discover something amazing. Don't forget to write down what you learn in your science journal!",
    ]
    
    # Use question hash to consistently pick same encouragement for same question
    import hashlib
    hash_num = int(hashlib.md5(q_lower.encode()).hexdigest(), 16)
    return encouragement_responses[hash_num % len(encouragement_responses)]

st.set_page_config(page_title="CurioLab: Home", page_icon="🔬", layout="wide")

# ---------- load profile ----------
prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json","r"))
    except Exception:
        prof = {}
# defaults
prof.setdefault("name","Scientist")
prof.setdefault("language","English")
prof.setdefault("xp", 0)
prof.setdefault("streak_days", 0)
prof.setdefault("last_log_date", None)
prof.setdefault("badges", [])
prof.setdefault("experiments_completed", 0)

LANG = prof["language"]

# ---------- CSS ----------
apply_global_theme()

# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### Scientist Homebase")
    if prof.get("avatar") and os.path.exists(prof["avatar"]):
        st.image(prof["avatar"], width=100, caption=prof.get("name","Scientist"))
    else:
        st.markdown(f"**{prof.get('name','Scientist')}**")
    
    # Animated XP bar
    st.progress(min(prof["xp"] % 100, 100) / 100)
    st.caption(f"XP: {prof['xp']%100}/100 • Streak: {prof['streak_days']} days 🔥")
    
    # Achievement badges
    if prof.get("badges"):
        st.markdown("### Badges")
        badge_html = "".join([f'<span class="badge">{badge}</span>' for badge in prof["badges"][:3]])
        st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Quick links")
    try:
        st.page_link("pages/0_Get_Started.py", label="Get Started")
        st.page_link("pages/1_Missions_Hub.py", label="Missions")
        st.page_link("pages/5_Analysis_Lab.py", label="Analysis Lab")
    except Exception:
        st.caption("Pages will appear after setup.")

# ---------- Hero ----------
# Debug: Check if mascot exists
mascot_exists = os.path.exists("assets/dr_curio.png")
if not mascot_exists:
    mascot_exists = os.path.exists("dr_curio.png")
    mascot_path = "dr_curio.png" if mascot_exists else "assets/dr_curio.png"
else:
    mascot_path = "assets/dr_curio.png"

header_with_mascot(
    title="CurioLab",
    subtitle="A space where your questions grow into discoveries.",
    mascot_path=mascot_path,
    size_px=140,
)

# ---------- Live Stats Counter ----------
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="stats-counter">🌍 1,247</div><p style="text-align:center;color:#6b7c8a;font-size:0.85rem;">Scientists Worldwide<br><span style="font-size:0.75rem;opacity:0.7;">(Demo data)</span></p>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stats-counter">🧫 {prof["experiments_completed"]}</div><p style="text-align:center;color:#6b7c8a;">Your Experiments</p>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stats-counter">⚡ {prof["xp"]}</div><p style="text-align:center;color:#6b7c8a;">Total XP</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Quick Experiment Button ----------
st.markdown('<div style="text-align:center;margin:32px 0;">', unsafe_allow_html=True)
if st.button("Run Your First Micro-Experiment: A quick 30-second challenge to get you started!", key="quick_exp", use_container_width=False):
    experiments = [
        "Blow on your hand with mouth open, then with lips pursed. Which feels cooler? Why?",
        "Look at a white surface through your fingers held close to your eye. See the diffraction?",
        "Hum and plug/unplug your ears. Notice how the sound changes!",
        "Drop water on different surfaces. Which spreads most? That's surface tension!",
        "Touch metal and wood. They have the same temperature but metal feels colder. That's thermal conductivity!",
    ]
    st.info(random.choice(experiments))
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Daily challenge (interactive flip card) ----------
st.markdown("<br>", unsafe_allow_html=True)

daily_options = [
    ("Measure temperature 3 times today", "Tip: Check morning, noon, and evening. Notice the pattern?"),
    ("Observe cloud types for 10 minutes", "Tip: Cumulus = fluffy, Stratus = flat layers, Cirrus = wispy!"),
    ("Sketch 3 different leaves you find", "Tip: Look at the edges, veins, and shape. Are they symmetrical?"),
    ("Count bees or butterflies for 10 minutes", "Tip: Stay still and quiet. What flowers do they visit most?"),
]
random.seed(dt.date.today().toordinal())
daily, tip = random.choice(daily_options)

# Use session state for flip
if 'challenge_flipped' not in st.session_state:
    st.session_state.challenge_flipped = False

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(
        f"""
        <div class="daily-challenge">
            <h3 style="margin:0 0 12px 0;"> Daily Challenge</h3>
            <p style="margin:0;font-size:1.05rem;font-weight:500;">{daily}</p>
            <p style="margin:12px 0 0 0;font-size:0.9rem;color:#8b7a3d;font-style:italic;">{tip if st.session_state.challenge_flipped else 'Click the button to reveal a tip!'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    if st.button("💡 Get Tip" if not st.session_state.challenge_flipped else "🎯 Got it!", key="flip_challenge"):
        st.session_state.challenge_flipped = not st.session_state.challenge_flipped
        st.rerun()

# ---------- Streak Calendar ----------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📅 Your Research Streak")
st.caption("Keep logging data every day to maintain your streak!")

# Simple 7-day streak visualization
today = dt.date.today()
streak_html = '<div class="streak-calendar">'
for i in range(6, -1, -1):
    day = today - dt.timedelta(days=i)
    is_active = i <= prof.get("streak_days", 0)
    day_class = "active" if is_active else "inactive"
    streak_html += f'<div class="streak-day {day_class}">{day.strftime("%a")[0]}</div>'
streak_html += '</div>'
st.markdown(streak_html, unsafe_allow_html=True)

# ---------- Missions (clean cards) ----------
st.markdown("<br><br>", unsafe_allow_html=True)

# ---------- Recent Discoveries Carousel ----------
st.markdown("### Recent Discoveries")
st.caption("See what other scientists are discovering! (Example data for demo)")

discovery_tabs = st.tabs(["🌍 Today", "📅 This Week", "🏆 Top Rated"])

with discovery_tabs[0]:
    discoveries_today = [
        "**Bob** discovered temperature drops 5°C at sunset in Phoenix!",
        "**Sarah** observed their bean plant grew 3cm in just 2 days!",
        "**John** counted 47 bees visiting lavender in 10 minutes!",
    ]
    for disc in discoveries_today:
        st.markdown(f"- {disc}")

with discovery_tabs[1]:
    discoveries_week = [
        "**Lisa** tracked rainfall patterns and predicted the next storm!",
        "**Kai** identified 8 different butterfly species in their backyard!",
        "**Chloe** documented all 10 cloud types in a single week!",
    ]
    for disc in discoveries_week:
        st.markdown(f"- {disc}")

with discovery_tabs[2]:
    discoveries_top = [
        "**Jane** created a complete weather station from recycled materials!",
        "**Bill** grew plants in 5 different conditions to test photosynthesis!",
        "**Amelia** built a bee hotel and documented 12 different species!",
    ]
    for disc in discoveries_top:
        st.markdown(f"- {disc}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Challenge Friends Feature ----------
st.markdown("###Challenge a Friend")
col1, col2 = st.columns([2, 1])
with col1:
    st.text_input("Enter friend's email", placeholder="scientist@curiolab.org", key="friend_email")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Send Challenge", key="send_challenge"):
        st.success("Challenge sent! 🎯")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Leaderboard Preview ----------
st.markdown("### 🏆 Top Scientists This Week")
st.caption("Example leaderboard - compete with scientists around the world!")

# Use columns for cleaner display
lb_data = [
    ("🥇", "Dr.Curio", 450, "🔥 12 day streak"),
    ("🥈", "Ariel", 380, "🌱 Plant Expert"),
    ("🥉", "Mary, 320, "🐝 Bee Whisperer"),
    ("4️⃣", "You!", prof["xp"], f"💪 {prof['streak_days']} day streak"),
    ("5️⃣", "Bill", 280, "🌡️ Weather Pro"),
]

# Create a container with clean styling
st.markdown("""
<style>
.leaderboard-container {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(90,138,158,0.08);
}
.lb-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
}
.lb-row.highlight {
    background: linear-gradient(135deg,#fff9e6 0%,#fffef5 100%);
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

for rank, name, xp, badge in lb_data:
    if name == "You!":
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff9e6 0%,#fffef5 100%);border-radius:12px;padding:12px;margin:8px 0;display:flex;justify-content:space-between;align-items:center;font-weight:600;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:1.5rem;">{rank}</span>
                <span>{name}</span>
                <span style="font-size:0.85rem;color:#6b7c8a;">{badge}</span>
            </div>
            <span style="color:#7eb8d1;">{xp} XP</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
        with col1:
            st.markdown(f"**{rank}**")
        with col2:
            st.markdown(f"**{name}**")
        with col3:
            st.caption(badge)
        with col4:
            st.markdown(f"**{xp} XP**")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Onboarding Checklist ----------
st.markdown("### ✅ Getting Started Checklist")
checklist_items = [
    ("Complete your first mission", prof.get("experiments_completed", 0) > 0),
    ("Set up your profile", bool(prof.get("name") != "Scientist")),
    ("Log data 3 days in a row", prof.get("streak_days", 0) >= 3),
    ("Ask Science Buddy a question", False),  # Could track this
    ("Earn your first badge", len(prof.get("badges", [])) > 0),
]

progress = sum([1 for _, done in checklist_items if done])
st.progress(progress / len(checklist_items))
st.caption(f"{progress}/{len(checklist_items)} completed")

checklist_html = '<div style="margin:16px 0;">'
for task, done in checklist_items:
    icon = "✅" if done else "⬜"
    style = "text-decoration:line-through;color:#aaa;" if done else ""
    checklist_html += f'<div style="padding:8px 0;{style}">{icon} {task}</div>'
checklist_html += '</div>'
st.markdown(checklist_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### 🧭 {t('Missions', LANG)}")
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🌤️ Air & Weather</h4>
            <p style="margin:0 0 24px 0;font-size:0.95rem;">Log temperature, rainfall, and PM2.5. Get an AI mini report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/2_Air_Quality.py", label=t("Open module →", LANG), icon="🌤️")

with c2:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🌱 Seeds & Growth</h4>
            <p style="margin:0 0 24px 0;font-size:0.95rem;">Track plant height and discover growth patterns.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/3_Seeds_Growth.py", label=t("Open module →", LANG), icon="🌱")

with c3:
    st.markdown(
        """
        <div class="card">
            <h4 style="margin:0 0 12px 0;">🐝 Pollinator Patrol</h4>
            <p style="margin:0 0 24px 0;font-size:0.95rem;">Count bees & butterflies to study biodiversity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/4_Pollinator_Patrol.py", label=t("Open module →", LANG), icon="🐝")

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------- Random Science Fact ----------
st.markdown("### Did You Know?")
facts = [
    "A butterfly's wings are actually transparent! The colors come from light reflecting off tiny scales.",
    "Plants can 'hear' water flowing underground and grow their roots toward it!",
    "Lightning is 5 times hotter than the surface of the Sun!",
    "Bees can recognize human faces and remember them for days!",
    "If you could fold a paper 42 times, it would reach the Moon!",
    "There are more bacteria in your body than stars in the Milky Way galaxy!",
    "You can never see a full rainbow - it's always a circle, but the ground blocks the bottom half!",
]
random.seed(dt.date.today().toordinal() + 1)  # Different seed than daily challenge
st.info(random.choice(facts))

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Science Buddy (chat) ----------
st.markdown("---")
st.subheader("🤖 Science Buddy")
st.caption("Ask simple questions and get friendly, accurate explanations.")

q = st.chat_input("Ask your Science Buddy (e.g., Why are plants green?)")
if q:
    response = get_science_buddy_response(q)
    st.chat_message("assistant").write(response)

q = st.chat_input("Ask your Science Buddy (e.g., Why are plants green?)")
if q:
    # ... all the OpenAI code ...

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Built with curiosity by Charlize S. ❤️✨")
