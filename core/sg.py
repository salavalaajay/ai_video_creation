import re

def split_into_scenes(script):
    sentences = re.split(r'(?<=[.!?।])\s+', script.strip())

    scenes = []
    current = []
    word_count = 0
    scene_num = 1

    for s in sentences:
        words = len(s.split())
        current.append(s)
        word_count += words

        if word_count >= 40:
            scenes.append({
                "scene_num": scene_num,
                "text": " ".join(current)
            })
            current = []
            word_count = 0
            scene_num += 1

    if current:
        scenes.append({
            "scene_num": scene_num,
            "text": " ".join(current)
        })

    return scenes