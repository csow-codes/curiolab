# pages/0_Get_Started.py
import streamlit as st, json, os, random, glob
from PIL import Image, ImageDraw

st.set_page_config(page_title="Get Started!", page_icon="🔬", layout="wide")

def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

ASSET_ROOT = "assets/avatar_parts/canvas_128"
LAYER_ORDER = ["base","eyes","mouth","hair","outfit","accessory","sticker"]
SAVE_DIR = "assets/avatars"; os.makedirs(SAVE_DIR, exist_ok=True)

def list_options(layer):
    p = os.path.join(ASSET_ROOT, layer)
    return sorted(glob.glob(os.path.join(p,"*.png"))) if os.path.exists(p) else []

def open_rgba(fp): return Image.open(fp).convert("RGBA")
def compose_avatar(choices):
    base_img = None
    for layer in LAYER_ORDER:
        fp = choices.get(layer); 
        if fp: base_img = open_rgba(fp); break
    if base_img is None: return None
    canvas = Image.new("RGBA", base_img.size, (0,0,0,0))
    for layer in LAYER_ORDER:
        fp = choices.get(layer)
        if fp: canvas = Image.alpha_composite(canvas, open_rgba(fp))
    return canvas

def fallback_avatar(seed_text="Scientist", size=8, scale=16):
    random.seed(seed_text)
    img = Image.new("RGB",(size,size),"white"); draw=ImageDraw.Draw(img)
    colors=[(55,148,255),(80,200,120),(250,180,70),(165,120,255)]
    for y in range(size):
        for x in range(size//2):
            c = random.choice(colors) if random.random()>0.35 else (240,240,240)
            draw.point((x,y),fill=c); draw.point((size-1-x,y),fill=c)
    return img.resize((size*scale,size*scale), Image.NEAREST).convert("RGBA")

prof = {}
if os.path.exists("profile.json"):
    try: prof = json.load(open("profile.json","r"))
    except Exception: prof = {}

st.markdown("## Get Started: Create Your Scientist Profile")
cute_box("Your profile saves locally. Choose your avatar! ✨")

left, right = st.columns([1,1.2], gap="large")

with left:
    name = st.text_input("Your name or nickname", value=prof.get("name", "Alex"))

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

    # simple fallback avatar (works even without assets)
    if st.button("✨ Generate avatar"):
        img = fallback_avatar(name)
        up = img.resize((img.width*3, img.height*3), Image.NEAREST)
        st.image(up, caption="Preview", use_container_width=False)
        avatar_path = os.path.join(SAVE_DIR, f"{name.lower().replace(' ','_')}.png")
        img.save(avatar_path)
        prof_new = {
            "name": name, "age": age, "topics": topics, "language": language,
            "avatar": avatar_path,
            "xp": prof.get("xp", 0), "streak_days": prof.get("streak_days", 0),
            "last_log_date": prof.get("last_log_date", None)
        }
        json.dump(prof_new, open("profile.json","w"))
        st.success("Saved! Now open "Missions" to explore.")
        st.balloons()

with right:
    st.markdown("Why we collect observations")
    st.write("Scientists look for patterns across days. When you log data consistently, you can make claims and test them. With friendly charts and a mini report, LearnLab helps you do both.")




