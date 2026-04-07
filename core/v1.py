from PIL import Image, ImageDraw
import os, requests, urllib.parse, random, time, textwrap

def create_scene_visuals(scenes, topic, output_dir="temp_assets"):
    os.makedirs(output_dir, exist_ok=True)
    paths = []

    headers = {'User-Agent': 'Mozilla/5.0'}

    for scene in scenes:
        path = os.path.join(output_dir, f"scene_{scene['scene_num']}.jpg")
        success = False

        try:
            prompt = f"{scene['text']}, {topic}, cinematic, 4k"
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&seed={random.randint(1,99999)}"
            time.sleep(1)

            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                open(path, "wb").write(r.content)
                success = True
        except:
            pass

        if not success:
            img = Image.new("RGB", (1280, 720), (30, 34, 43))
            d = ImageDraw.Draw(img)
            text = textwrap.fill(scene['text'], 40)
            d.text((50, 300), text, fill="white")
            img.save(path)

        paths.append(path)

    return paths