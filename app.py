import streamlit as st
import os, shutil

from core.script_generator import generate_script
from core.sg import split_into_scenes
from core.v1 import create_scene_visuals
from core.v2 import generate_voiceover
from core.v3 import assemble_video

st.set_page_config(page_title="Script to Screen", layout="wide")

st.title("🎬 Script to Screen")

topic = st.text_input("Topic", "Solar Energy")
video_type = st.selectbox("Type", ["Educational", "Marketing", "Story"])
duration = st.selectbox("Duration", ["1 Minute", "3 Minutes", "5 Minutes"])
language = st.selectbox("Language", ["English", "Hindi", "Spanish"])

if st.button("Generate Video"):

    # Clean temp
    if os.path.exists("temp_assets"):
        shutil.rmtree("temp_assets")

    os.makedirs("temp_assets", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    with st.spinner("Generating video..."):

        script = generate_script(topic, video_type, duration, language)
        scenes = split_into_scenes(script)
        visuals = create_scene_visuals(scenes, topic)
        audio = generate_voiceover(scenes, language)

        output = f"outputs/{topic.replace(' ', '_')}.mp4"
        assemble_video(visuals, audio, output)

    st.success("Video Generated!")
    st.video(output)