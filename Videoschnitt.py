#***Videoschnitt***
import os
import random
from textwrap import wrap

from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeAudioClip,VideoFileClip
from pydub import AudioSegment

import srt
import math
from PIL import Image
import numpy as np

# Subtitle
def create_subtitles_clip(sub, color_fg, fontsize=40, font='Orbitron-VariableFont_wght', video_width=1920, color_bg='black'):

    wrapped_content_lines = wrap(sub.content.upper(), width=video_width//fontsize)
    wrapped_content = "\n".join(wrapped_content_lines)

    txt_clip_fg = TextClip(wrapped_content, fontsize=fontsize, font=font, color=color_fg, stroke_color=color_fg, stroke_width=3, size=(video_width, 1000), method="caption")
    txt_clip_fg = txt_clip_fg.set_pos(('center'))

    txt_clip_bg = TextClip(wrapped_content, fontsize=fontsize, font=font, color=color_bg, stroke_color=color_bg, stroke_width=12, size=(video_width, 1000), method="caption")
    txt_clip_bg = txt_clip_bg.set_pos(('center'))

    txt_clip = CompositeVideoClip([txt_clip_bg, txt_clip_fg])

    start_time = timedelta_to_seconds(sub.start)
    end_time = timedelta_to_seconds(sub.end)
    txt_clip = txt_clip.set_start(start_time).set_duration(end_time - start_time)

    return txt_clip

def convert_srt_to_subtitles(srt_file_path, fontsize=40, font='Orbitron-VariableFont_wght', video_width=1920):
    # Auswahl der Farbe hier
    colors = ['#ffff00', '#caff70', '#8a2be2', '#ff0000', '#ff1493', '#ffa500', '#8ee5ee', '#008b8b', '#7cfc00', '#4eee94', '#cd3278', '#9a32cd', '#9f79ee', '#ffb90f']
    color_fg = random.choice(colors)

    with open(srt_file_path) as f:
        subtitle_generator = srt.parse(f)
        subtitles = list(subtitle_generator)

    subtitle_clips = []
    for sub in subtitles:
        txt_clip = create_subtitles_clip(sub, color_fg, fontsize=fontsize, font=font, video_width=video_width)
        subtitle_clips.append(txt_clip)

    return subtitle_clips

def timedelta_to_seconds(timedelta):
    return timedelta.seconds + timedelta.microseconds / 1E6

# ***Zoom-Effekt****
def zoom_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # Die neuen Dimensionen müssen gerade sein
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = np.array(img)
        img.close()

        return result

    return clip.fl(effect)

def create_video(image_files, audio_path, srt_path, background_music, projekt_ordner):
    # Bei der Erstellung der ImageClips:
    clips = [zoom_effect(ImageClip(im).set_duration(10).crossfadein(0.3).crossfadeout(0.3)) for im in image_files]

    # Video width
    video_width = clips[0].w  # Get the width of the first image clip

    # Pfad zur subtitles.srt-Datei im Projektordner
    subtitle_clips = convert_srt_to_subtitles(srt_path, video_width=video_width)

    # Erstelle einen VideoClip aus den Bildclips
    video = concatenate_videoclips(clips, method="compose")

    # Lege die Untertitel über den VideoClip
    video = CompositeVideoClip([video] + subtitle_clips)

    # ***Funktion, um Reverb auf eine Audiodatei anzuwenden,***
    # Die generierte Audiodatei
    wav_audio_path = audio_path.replace('.mp3', '.wav')

    # Konvertiere MP3 zu WAV
    audio = AudioSegment.from_mp3(audio_path)
    audio.export(wav_audio_path, format='wav')

    # Wende Reverb mit SoX an
    reverb_audio_path = os.path.join(projekt_ordner, "geschichte_audio_reverb.wav")
    # reverb [reverberance (50%) [HF-damping (50%)] [room-scale (100%)] [stereo-depth (100%)] [pre-delay (0ms)] [wet-gain (0dB)] [wet-only (no)]]
    os.system(f'sox "{wav_audio_path}" "{reverb_audio_path}" reverb 25 100 50')

    # Lade die bearbeitete Audiodatei
    audio_clip = AudioFileClip(reverb_audio_path)

    # Die Hintergrundmusik und die Sprachaufnahme zum Video hinzufügen
    final_audio = CompositeAudioClip([audio_clip, background_music])
    video = video.set_audio(final_audio)

    # Video auf die Länge der Audiodatei + 2 Sekunden setzen
    video = video.set_duration(audio_clip.duration + 2)

    # Das Video speichern
    main_video_path = os.path.join(projekt_ordner, "video_with_subtitles.mp4")
    video.write_videofile(main_video_path, codec='libx264', audio_codec='aac', fps=30)

    # Pfad zum animierten Logo
    mov_logo_path = VideoFileClip('C:/Users/NightCoffe/Desktop/AutoInsta/Logo/Logo_Green.jpg.mov', has_mask=True)

    # Skaliere das Logo-Video und setze seine Position
    mov_logo_path = mov_logo_path.resize(height=300)
    mov_logo_path = mov_logo_path.set_position(('center', 'bottom'))

    # Füge das Logo-Video zum Hauptvideo hinzu
    main_video_path = VideoFileClip(main_video_path)
    final_clip = CompositeVideoClip([main_video_path, mov_logo_path.set_duration(main_video_path.duration)])

    # Speichere das resultierende Video
    final_clip_path = os.path.join(projekt_ordner, "final_video.mp4")
    final_clip.write_videofile(final_clip_path)


    return final_clip_path