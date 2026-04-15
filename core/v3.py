from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

def assemble_video(visual_paths, audio_paths, output_path="final_video.mp4"):
    clips = []

    for img, audio in zip(visual_paths, audio_paths):
        a = AudioFileClip(audio)

        c = (
            ImageClip(img)
            .with_size((1280, 720))
            .set_duration(a.duration)
            .set_audio(a)
            .fadein(0.5)
            .fadeout(0.5)
        )

        clips.append(c)

    final = concatenate_videoclips(clips, method="compose")

    final.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None
    )

    final.close()
    return output_path
