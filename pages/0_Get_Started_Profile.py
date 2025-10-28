import streamlit as st, json, os, random, glob
from PIL import Image, ImageDraw

# --- cute UI helpers ---
def cute_box(text: str, bg="#f8f4ff"):
    st.markdown(
        f"""
        <div style="
            background-color:{bg};
            padding:12px 14px;
            border-radius:16px;
            border:1px solid #ede9fe;
            line-height:1.5;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


st.title("Get Started — Create Your Scientist")
st.caption("Customize your own avatar.")

# --------------------------
# Config: where parts live
# --------------------------
ASSET_ROOT = "assets/avatar_parts/canvas_128"  # change if you use another folder/size
LAYER_ORDER = ["base", "eyes", "mouth", "hair", "outfit", "accessory", "sticker"]  # draw bottom → top
SAVE_DIR = "assets/avatars"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------
# Helpers
# --------------------------
def list_options(layer_name: str):
    """Return a sorted list of file paths for a layer (or empty if none)."""
    path = os.path.join(ASSET_ROOT, layer_name)
    return sorted(glob.glob(os.path.join(path, "*.png"))) if os.path.exists(path) else []

def filename_to_label(fp: str):
    """Turn 'assets/.../hair01.png' into 'hair01' → human label 'Hair 01'."""
    base = os.path.basename(fp)
    name = os.path.splitext(base)[0]  # hair01
    prefix = "".join([c for c in name if not c.isdigit()]) or name  # hair
    digits = "".join([c for c in name if c.isdigit()])
    hn = prefix.capitalize()
    return f"{hn} {digits or ''}".strip()

def open_rgba(fp: str):
    img = Image.open(fp).convert("RGBA")
    return img

def compose_avatar(choices: dict):
    """Composite selected layer PNGs in order; return RGBA image (pixel crisp)."""
    # find a canvas size using the first available image
    base_img = None
    for layer in LAYER_ORDER:
        fp = choices.get(layer)
        if fp:
            base_img = open_rgba(fp)
            break
    if base_img is None:
        return None
    canvas = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    # draw in order
    for layer in LAYER_ORDER:
        fp = choices.get(layer)
        if fp:
            layer_img = open_rgba(fp)
            canvas = Image.alpha_composite(canvas, layer_img)
    return canvas

# Fallback: simple mirrored pixel pattern avatar (works even with no assets)
def fallback_avatar(seed_text="Scientist", size=8, scale=16):
    random.seed(seed_text)
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    colors = [(55,148,255), (80,200,120), (250,180,70), (165,120,255)]
    for y in range(size):
        for x in range(size // 2):
            c = random.choice(colors) if random.random() > 0.35 else (240,240,240)
            draw.point((x, y), fill=c)
            draw.point((size - 1 - x, y), fill=c)
    img = img.resize((size * scale, size * scale), Image.NEAREST)
    return img.convert("RGBA")

def have_any_assets():
    return any(list_options(layer) for layer in LAYER_ORDER)

# --------------------------
# Profile inputs (left)
# --------------------------
col_left, col_right = st.columns([1, 1.2])

with col_left:
    name = st.text_input("Your name or nickname", value="Alex")
    age = st.selectbox("Age range", ["8–10","11–13","14–16"])
    topics = st.multiselect("Favorite topics", ["Environment","Plants","Weather","Health","Physics","Space"])

    st.markdown("### (˶˃ᆺ˂˶) Avatar builder")

    # Build the selection lists for each layer
    layer_choices = {}
    for layer in LAYER_ORDER:
        files = list_options(layer)
        if files:
            labels = [filename_to_label(fp) for fp in files]
            default_idx = 0
            picked = st.selectbox(f"{layer.capitalize()}", labels, index=default_idx, key=f"sel_{layer}")
            layer_choices[layer] = files[labels.index(picked)]
        else:
            layer_choices[layer] = None  # layer may be optional

    # Surprise me: pick random available file for each layer
    if st.button("✨ Surprise me!"):
        for layer in LAYER_ORDER:
            files = list_options(layer)
            layer_choices[layer] = random.choice(files) if files else None
        st.session_state["surprise_avatar"] = layer_choices
    if "surprise_avatar" in st.session_state:
        layer_choices = st.session_state["surprise_avatar"]

    # Save button
    if st.button("Save Profile"):
        # Compose final avatar (either from layers or fallback)
        if have_any_assets():
            final_img = compose_avatar(layer_choices)
            if final_img is None:
                final_img = fallback_avatar(name)
        else:
            final_img = fallback_avatar(name)

        avatar_path = os.path.join(SAVE_DIR, f"{name.lower().replace(' ','_')}.png")
        final_img.save(avatar_path)

        with open("profile.json","w") as f:
            json.dump({"name": name, "age": age, "topics": topics, "avatar": avatar_path}, f)

        st.success("Profile saved! Open the **Modules** page to pick a topic.")
        st.balloons()

# --------------------------
# Live preview (right)
# --------------------------
with col_right:
    st.markdown("### Live preview")
    if have_any_assets():
        preview_img = compose_avatar(layer_choices)
        if preview_img is None:
            preview_img = fallback_avatar(name)
    else:
        st.info("No avatar parts found yet. Add PNG layers in `assets/avatar_parts/canvas_128/...`.\n"
                "Using a cute fallback for now ✨")
        preview_img = fallback_avatar(name)

    # Upscale for crisp pixels on screen
    scale_preview = 3
    preview_up = preview_img.resize((preview_img.width * scale_preview,
                                     preview_img.height * scale_preview),
                                     Image.NEAREST)
    st.image(preview_up, caption="Your pixel scientist", use_container_width=False)

    # Optional: download button (saves what you see)
    st.download_button("⬇️ Download avatar PNG", data=preview_img.tobytes(), file_name=f"{name}_avatar.raw",
                       help="(Tip: your profile is saved as a PNG automatically in assets/avatars/)")
