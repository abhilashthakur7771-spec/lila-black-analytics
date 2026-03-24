import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageDraw

# --- PAGE CONFIG ---
st.set_page_config(page_title="LILA BLACK Analytics", layout="wide")
st.title("🎮 LILA BLACK: Product Insights Suite")

# The Rulebook for Ambrose Valley, Grand Rift, and Lockdown
MAP_CONFIGS = {
    "AmbroseValley": {"scale": 900, "origin_x": -370, "origin_z": -473, "img": "minimaps/AmbroseValley_Minimap.png"},
    "GrandRift": {"scale": 581, "origin_x": -290, "origin_z": -290, "img": "minimaps/GrandRift_Minimap.png"},
    "Lockdown": {"scale": 1000, "origin_x": -500, "origin_z": -500, "img": "minimaps/Lockdown_Minimap.jpg"}
}

@st.cache_data(show_spinner=False)
def load_match_data(file_path):
    df = pd.read_parquet(file_path)
    # Decode binary event names into human-readable strings
    df['event'] = df['event'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
    # Create a 'Step' column so the slider works even for 0-second matches
    df['step'] = range(len(df))
    return df

def get_pixel_coords(x, z, config):
    # Standard normalization: (Point - Origin) / Total Scale
    u = (x - config['origin_x']) / config['scale']
    v = (z - config['origin_z']) / config['scale']
    
    # Validation: Is the player actually inside the playable minimap area?
    on_map = 0 <= u <= 1 and 0 <= v <= 1
    
    # Convert to 1024x1024 pixel space
    px = u * 1024
    py = (1 - v) * 1024
    return px, py, on_map

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("Navigation")
    date_folders = sorted([f for f in os.listdir("player_data") if os.path.isdir(os.path.join("player_data", f))])
    selected_day = st.selectbox("1. Select Date", date_folders)
    
    folder_path = os.path.join("player_data", selected_day)
    files = sorted(os.listdir(folder_path))
    
    st.divider()
    show_heatmap = st.checkbox("🔥 GLOBAL DEATH HEATMAP", help="Aggregates ALL matches to find choke points")
    
    if not show_heatmap:
        selected_file = st.selectbox("2. Select Individual Match", files)

# --- THE ENGINE ---
# Auto-detect map from the first file in the folder
sample_df = load_match_data(os.path.join(folder_path, files[0]))
map_name = sample_df['map_id'].iloc[0]
config = MAP_CONFIGS.get(map_name, MAP_CONFIGS["AmbroseValley"])

# Prepare the visual layers
base_img = Image.open(config['img']).convert("RGBA")
overlay = Image.new("RGBA", base_img.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

if show_heatmap:
    # --- MACRO VIEW: Aggregate Data ---
    with st.spinner('Scanning match history for death clusters...'):
        for f in files[:75]: # Scanning 75 files for a representative sample
            try:
                m_df = pd.read_parquet(os.path.join(folder_path, f))
                # Filter for death events in byte format for speed
                deaths = m_df[m_df['event'].isin([b'Killed', b'BotKilled'])]
                for d in deaths.itertuples():
                    px, py, on_map = get_pixel_coords(d.x, d.z, config)
                    if on_map:
                        # Draw a semi-transparent 'heat' circle
                        draw.ellipse([px-12, py-12, px+12, py+12], fill=(255, 0, 0, 70))
            except: continue
    
    # Safe Merge: Overlay on top of Map
    st.subheader(f"Global Death Hotspots: {selected_day}")
    st.image(Image.alpha_composite(base_img, overlay), use_container_width=True)
    st.caption("Darker red areas indicate 'Choke Points' where multiple players have died.")

elif selected_file:
    # --- MICRO VIEW: Single Player Journey ---
    df = load_match_data(os.path.join(folder_path, selected_file))
    
    # Steps Slider (Playback)
    max_step = len(df) - 1
    step_limit = st.slider("Match Playback (Step-by-Step)", 0, max_step, max_step)
    current_df = df.iloc[:step_limit + 1]

    path_coords = []
    off_map_points = 0
    
    for r in current_df.itertuples():
        px, py, on_map = get_pixel_coords(r.x, r.z, config)
        if not on_map: off_map_points += 1
        
        if 'Position' in r.event:
            path_coords.append((px, py))
        
        # Visual Event Markers
        if 'Kill' in r.event:
            draw.ellipse([px-10, py-10, px+10, py+10], fill=(0, 255, 0, 255), outline="white")
        elif 'Killed' in r.event:
            draw.polygon([(px, py-12), (px-10, py+8), (px+10, py+8)], fill=(255, 0, 0, 255))

    # Connect the dots with the journey line
    if len(path_coords) > 1:
        draw.line(path_coords, fill=(0, 255, 255, 255), width=4)

    # Display Columns
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Total Events", len(df))
        if off_map_points > 0:
            st.warning(f"⚠️ {off_map_points} events are 'Off-Map' (Waiting Area/Lobby)")
        st.write("**Legend:**")
        st.write("🟢 Kill | 🔺 Death | 🟦 Path")
        st.dataframe(current_df[['event', 'x', 'z']].tail(5), hide_index=True)
    
    with col2:
        st.image(Image.alpha_composite(base_img, overlay), use_container_width=True)