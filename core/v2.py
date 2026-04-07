import os, asyncio, edge_tts, re

async def _gen(text, voice, path):
    text = re.sub(r'\s+', ' ', text)
    tts = edge_tts.Communicate(text, voice, rate="+5%")
    await tts.save(path)

async def _batch(tasks):
    await asyncio.gather(*tasks)

def generate_voiceover(scenes, language, output_dir="temp_assets"):
    os.makedirs(output_dir, exist_ok=True)

    voice_map = {
        "English": "en-US-AriaNeural",
        "Spanish": "es-ES-ElviraNeural",
        "Hindi": "hi-IN-SwaraNeural"
    }

    voice = voice_map.get(language, "en-US-AriaNeural")

    tasks, paths = [], []

    for s in scenes:
        path = os.path.join(output_dir, f"audio_{s['scene_num']}.mp3")
        tasks.append(_gen(s['text'], voice, path))
        paths.append(path)

    asyncio.run(_batch(tasks))
    return paths