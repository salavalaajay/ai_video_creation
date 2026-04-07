from openai import OpenAI

def generate_script(topic, video_type, duration, language, api_key=None):
    base = [
        f"Welcome to this {video_type.lower()} video about {topic}.",
        f"Today we explore how {topic} impacts our lives.",
        f"Understanding {topic} is important.",
        f"It has many real world applications.",
        f"There are challenges to overcome.",
        f"In the future, we expect more innovation.",
        f"Thank you for watching."
    ]

    duration_map = {"1 Minute": 160, "3 Minutes": 480, "5 Minutes": 800}
    target = duration_map.get(duration, 160)

    script, count, i = [], 0, 0

    while count < target:
        s = base[i % len(base)]
        w = len(s.split())
        if count + w > target:
            break
        script.append(s)
        count += w
        i += 1

    return " ".join(script)