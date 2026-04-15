from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os


def assemble_video(images, audios, output_path):
    clips = []

    print("Images:", images)
    print("Audios:", audios)

    # safety check
    if not images or not audios:
        raise RuntimeError("Empty images or audios list")

    if len(images) != len(audios):
        print("WARNING: mismatch, trimming to shortest length")
        n = min(len(images), len(audios))
        images = images[:n]
        audios = audios[:n]

    for i, (img_path, audio_path) in enumerate(zip(images, audios)):
        try:
            if not os.path.exists(img_path):
                print(f"Missing image {img_path}")
                continue

            if not os.path.exists(audio_path):
                print(f"Missing audio {audio_path}")
                continue

            audio = AudioFileClip(audio_path)

            clip = (
                ImageClip(img_path)
                .set_duration(audio.duration)
                .set_audio(audio)
            )

            clips.append(clip)

        except Exception as e:
            print(f"Clip error {i}: {e}")

    if len(clips) == 0:
        raise RuntimeError("No valid clips created (all scenes failed)")

    final_video = concatenate_videoclips(clips, method="compose")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path
