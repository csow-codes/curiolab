import streamlit as st, json, os, random, glob
from PIL import Image, ImageDraw

st.set_page_config(page_title="Get Started", page_icon="🤩", layout="wide")

# ---------- cute helpers ----------
def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"<div style='background:{bg};padding:14px 18px;border-radius:16px;border:1px solid #ede9fe;line-height:1.55'>{text}</div>",
        unsafe_allow_html=True
    )

# ---------- avatar parts (optional, safe fallback) ----------
ASSET_ROOT = "assets/avatar_parts/canvas_128"
LAYER_ORDER = ["base","eyes","mouth","hair","outfit","accessory","sticker"]
SAVE_DIR = "assets/avatars"
os.makedirs(SAVE_DIR, exist_ok=True)

def list_options(layer): 
    path = os.path.join(ASSET_ROOT, layer)
    return sorted(glob.glob(os.path.join(path,"*.png"))) if os.path.exists(path) else []

def open_rgba(fp): return Image.open(fp).convert("RGBA")

def compose_avatar(choices):
    base_img = None
    for layer in LAYER_ORDER:
        fp = choices.get(layer)
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

def have_any_assets(): 
    return any(list_options(layer) for layer in LAYER_ORDER)

# ---------- load existing profile ----------
prof = {}
if os.path.exists("profile.json"):
    try:
        prof = json.load(open("profile.json","r"))
    except Exception:
        prof = {}

st.markdown("## Get Started: Create Your Scientist Profile")
cute_box("Your profile saves locally (no logins needed). Avatars are **generated**, not photos (privacy-safe) ✨")

left, right = st.columns([1,1.2], gap="large")

with left:
    name = st.text_input("Your name or nickname", value=prof.get("name","Charlize"))
    age = st.selectbox("Age range", ["7–10","11–14","15–18"], index=(["7–10","11–14","15–18"].index(prof.get("age","11–14")) if prof.get("age") else 1))
    topics = st.multiselect("Favorite topics", ["Environment","Plants","Weather","Health","Physics","Space"], default=prof.get("topics",["Environment","Plants"]))
    language = st.selectbox("Language (UI labels)", ["English","简体中文","Español"], index={"English":0,"简体中文":1,"Español":2}.get(prof.get("language","English"),0))

    st.markdown("### (๑ > ᴗ < ๑) Avatar builder")
    # dropdowns if parts exist
    layer_choices = {}
    if have_any_assets():
        for layer in LAYER_ORDER:
            files = list_options(layer)
            if files:
                labels = [os.path.splitext(os.path.basename(f))[0] for f in files]
                idx = 0
                if prof.get("avatar_choice", {}).get(layer):
                    try: idx = files.index(prof["avatar_choice"][layer])
                    except: idx = 0
                pick = st.selectbox(layer.capitalize(), labels, index=idx, key=f"sel_{layer}")
                layer_choices[layer] = files[labels.index(pick)]
            else:
                layer_choices[layer] = None
        if st.button("✨ Surprise me!"):
            for layer in LAYER_ORDER:
                files = list_options(layer)
                layer_choices[layer] = random.choice(files) if files else None
            st.session_state["surprise"] = layer_choices
        if "surprise" in st.session_state:
            layer_choices = st.session_state["surprise"]
    else:
        cute_box("No avatar parts found yet — using a cute generated fallback. Add PNG layers later in `assets/avatar_parts/canvas_128/...`.")

    if st.button("💾 Save Profile", type="primary"):
        final_img = compose_avatar(layer_choices) if have_any_assets() else fallback_avatar(name)
        avatar_path = os.path.join(SAVE_DIR, f"{name.lower().replace(' ','_')}.png")
        final_img.save(avatar_path)
        prof_new = {
            "name": name, "age": age, "topics": topics, "language": language,
            "avatar": avatar_path,
            "avatar_choice": layer_choices if have_any_assets() else {},
            # progress/streak scaffolding
            "xp": prof.get("xp", 0),
            "streak_days": prof.get("streak_days", 0),
            "last_log_date": prof.get("last_log_date", None)
        }
        json.dump(prof_new, open("profile.json","w"))
        st.success("Saved! Open **Modules** to start exploring.")
        st.balloons()

with right:
    st.markdown("### Live preview")
    if have_any_assets(): img = compose_avatar(layer_choices)
    else: img = fallback_avatar(name)
    up = img.resize((img.width*3, img.height*3), Image.NEAREST)
    st.image(up, caption="Your pixel scientist", use_container_width=False)

    if os.path.exists("profile.json"):
        st.download_button("⬇️ Download saved avatar", data=open(prof.get("avatar"),"rb").read(), file_name=f"{name}_avatar.png")
