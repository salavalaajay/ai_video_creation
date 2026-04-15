from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import os


def assemble_video(images, audios, output_path):
    clips = []

    for img_path, audio_path in zip(images, audios):
        try:
            audio = AudioFileClip(audio_path)

            # FIX: NO ANTIALIAS
            clip = (
                ImageClip(img_path)
                .set_duration(audio.duration)
                .set_audio(audio)
                .resize((1280, 720))  # safe resize
            )

            clips.append(clip)

        except Exception as e:
            print(f"Clip error: {e}")

    if not clips:
        raise RuntimeError("No valid clips created")

    final_video = concatenate_videoclips(clips, method="compose")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path
