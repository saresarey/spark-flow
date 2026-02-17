import streamlit as st
import fal_client
import os
import requests
import random
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Page Configuration
st.set_page_config(page_title="SparkFlow Studio", page_icon="⚡", layout="wide")

# 3. CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    
    .title-text {
        font-size: 3rem; font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF9068);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .subtitle-text { font-size: 1.2rem; color: #555; margin-bottom: 30px; }
    
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF416C 100%);
        color: white; font-weight: 700; border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3); transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- ONBOARDING (TUTORIAL) ---
if "first_visit" not in st.session_state:
    st.session_state.first_visit = True

@st.dialog("🚀 Welcome to SparkFlow!")
def show_tutorial():
    st.markdown("""
    Ready to unleash your creativity? Here is a quick start guide:
    
    #### 1️⃣ Write a Prompt
    Describe your dream scene in detail (English works best). Mention lighting, colors, and mood.
    
    #### 2️⃣ Choose a Style
    Pick a vibe like **'Cinematic'** or **'Anime'** from the sidebar to instantly enhance your image.
    
    #### 3️⃣ What is 'Seed'? 🎲
    * **New Variation:** AI creates a totally new image every time.
    * **Lock Seed:** If you like a specific composition (pose, angle) but want to change small details, choose **'Lock Seed'**.
    """)
    
    if st.button("Got it, Let's Create! ⚡"):
        st.session_state.first_visit = False
        st.rerun()

if st.session_state.first_visit:
    show_tutorial()

# --- SESSION STATE (MEMORY) ---
if "history" not in st.session_state:
    st.session_state.history = [] 

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Studio Settings")
    st.write("---")
    
    style_option = st.selectbox(
        "🎨 Image Style", 
        ("Cinematic", "Anime", "Photorealistic", "3D Render", "Sketch", "None"),
        help="Defines the artistic vibe. Choose 'Cinematic' for movies, 'Anime' for cartoons."
    )
    
    aspect_ratio_map = {
        "16:9 Landscape": "landscape_16_9",
        "4:3 Landscape": "landscape_4_3",
        "1:1 Square": "square_hd",
        "4:3 Portrait": "portrait_4_3",
        "9:16 Portrait": "portrait_16_9"
    }
    selected_ratio_label = st.selectbox(
        "📐 Aspect Ratio", 
        options=list(aspect_ratio_map.keys()),
        help="Dimensions of the image. 16:9 is best for screens, 9:16 for phones."
    )
    selected_api_ratio = aspect_ratio_map[selected_ratio_label]

    st.write("---")
    st.markdown("##### 🧩 Consistency Control")
    
    mode = st.radio(
        "Generation Mode:",
        options=["🎲 New Variation (Random)", "🔒 Keep Composition (Lock Seed)"],
        index=0,
        help="Do you want a surprise every time, or do you want to refine the same scene?"
    )
    
    if mode == "🔒 Keep Composition (Lock Seed)":
        seed_input = st.number_input(
            "Seed ID", 
            value=42, 
            help="This number is the DNA of the image. Keeping it same preserves the structure."
        )
        use_random_seed = False
    else:
        use_random_seed = True

# --- MAIN INTERFACE ---
st.markdown('<p class="title-text">⚡ SparkFlow Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Transform your imagination into reality with AI.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 2], gap="large")

with col1:
    st.markdown("##### ✍️ Describe your vision")
    prompt_input = st.text_area(
        label="Prompt", label_visibility="collapsed", height=150, 
        placeholder="E.g., A futuristic cyberpunk detective standing in rain...",
        help="Describe the subject, lighting, and environment in English."
    )

    style_prompts = {
        "Cinematic": ", cinematic lighting, 8k resolution, highly detailed, dramatic atmosphere",
        "Anime": ", anime style, studio ghibli inspired, vibrant colors",
        "Photorealistic": ", 8k, raw photo, realistic texture, ray tracing",
        "3D Render": ", 3d render, unreal engine 5, octane render",
        "Sketch": ", charcoal sketch, pencil drawing, rough lines",
        "None": ""
    }
    
    final_prompt = prompt_input + style_prompts[style_option]
    st.write("")
    generate_btn = st.button("✨ GENERATE ARTWORK")

# --- GENERATION LOGIC ---
if generate_btn and prompt_input:
    api_key = os.getenv("FAL_KEY")
    if not api_key:
        st.error("❌ API Key missing. Check .env file.")
    else:
        with col2:
            with st.spinner("🎨 AI is crafting your masterpiece..."):
                try:
                    current_seed = random.randint(0, 1000000) if use_random_seed else int(seed_input)
                    
                    handler = fal_client.submit(
                        "fal-ai/flux/schnell",
                        arguments={
                            "prompt": final_prompt,
                            "image_size": selected_api_ratio,
                            "num_inference_steps": 4,
                            "seed": current_seed,
                            "enable_safety_checker": False
                        },
                    )
                    result = handler.get()
                    image_url = result["images"][0]["url"]
                    
                    st.session_state.history.insert(0, {
                        "url": image_url,
                        "prompt": prompt_input,
                        "style": style_option,
                        "seed": current_seed
                    })
                    
                except Exception as e:
                    st.error(f"Error: {e}")

# --- RESULT & HISTORY DISPLAY ---
with col2:
    if len(st.session_state.history) > 0:
        latest = st.session_state.history[0]
        st.image(latest["url"], use_container_width=True, caption=f"Seed: {latest['seed']} | Style: {latest['style']}")
        
        try:
            response = requests.get(latest["url"])
            img = Image.open(BytesIO(response.content))
            
            buf_png = BytesIO()
            img.save(buf_png, format="PNG")
            byte_png = buf_png.getvalue()
            
            buf_jpg = BytesIO()
            img.convert("RGB").save(buf_jpg, format="JPEG", quality=85)
            byte_jpg = buf_jpg.getvalue()

            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.download_button("⬇️ High-Res (PNG)", data=byte_png, file_name="sparkflow_hd.png", mime="image/png")
            with d_col2:
                st.download_button("⬇️ Web Ready (JPG)", data=byte_jpg, file_name="sparkflow_web.jpg", mime="image/jpeg")
                
        except Exception:
            pass

    elif not generate_btn:
        st.info("👈 Waiting for your creativity...")

# --- HISTORY GALLERY ---
if len(st.session_state.history) > 1:
    st.write("---")
    st.subheader("🕰️ Session History")
    history_cols = st.columns(3)
    for idx, item in enumerate(st.session_state.history[1:]):
        with history_cols[idx % 3]:
            st.image(item["url"], use_container_width=True)
            st.caption(f"🌱 Seed: {item['seed']}")