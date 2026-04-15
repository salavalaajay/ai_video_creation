from pathlib import Path
from typing import Iterable, List, Tuple

from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips


def assemble_video(
    images: Iterable[str],
    audios: Iterable[str],
    output_path: str = "output.mp4",
    size: Tuple[int, int] = (1280, 720),
    fps: int = 24,
    codec: str = "libx264",
    audio_codec: str = "aac",
) -> str:
    """Assemble a video from image and audio files.

    Each image is shown for the duration of its corresponding audio clip.
    """

    images_list: List[str] = list(images)
    audios_list: List[str] = list(audios)

    if not images_list:
        raise ValueError("No image files provided to assemble_video.")
    if not audios_list:
        raise ValueError("No audio files provided to assemble_video.")
    if len(images_list) != len(audios_list):
        raise ValueError(
            f"images and audios must have the same number of items: "
            f"{len(images_list)} image(s), {len(audios_list)} audio(s)."
        )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    clips = []
    audio_clips = []
    final_video = None

    try:
        for index, (img_path, aud_path) in enumerate(zip(images_list, audios_list), start=1):
            img_file = Path(img_path)
            aud_file = Path(aud_path)

            if not img_file.exists():
                print(f"Warning: image file not found, skipping clip {index}: {img_file}")
                continue
            if not aud_file.exists():
                print(f"Warning: audio file not found, skipping clip {index}: {aud_file}")
                continue

            audio_clip = None
            try:
                audio_clip = AudioFileClip(str(aud_file))
                clip = (
                    ImageClip(str(img_file))
                    .set_duration(audio_clip.duration)
                    .resize(newsize=size)
                    .set_audio(audio_clip)
                )

                audio_clips.append(audio_clip)
                clips.append(clip)

            except Exception as exc:
                print(f"Error processing pair {index} ({img_file}, {aud_file}): {exc}")
                if audio_clip is not None:
                    try:
                        audio_clip.close()
                    except Exception:
                        pass

        if not clips:
            raise RuntimeError(
                "No video clips could be created. Verify that input image and audio files exist and are valid."
            )

        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            str(output_file),
            fps=fps,
            codec=codec,
            audio_codec=audio_codec,
        )

        return str(output_file)

    finally:
        if final_video is not None:
            try:
                final_video.close()
            except Exception:
                pass

        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass

        for audio_clip in audio_clips:
            try:
                audio_clip.close()
            except Exception:
                pass
