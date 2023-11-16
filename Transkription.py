#***Transkription***
import os
from faster_whisper import WhisperModel

def format_srt_time(seconds):
    """Konvertiert eine Zeit in Sekunden in das SRT-Zeitformat."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = (seconds % 1) * 1000
    return "{:02}:{:02}:{:02},{:03d}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

def transcribe_audio_to_text(audio_path, projekt_ordner):
    model_size = "large-v2"
    model = WhisperModel(model_size, device="cuda", compute_type="int8")

    # Transkription der Audiodatei
    segments, info = model.transcribe(audio_path, word_timestamps=True)

    # Konvertierung des Generators in eine Liste
    segments = list(segments)

    # Sammelt die Wortinformationen
    wordlevel_info = []
    for segment in segments:
        for word in segment.words:
            wordlevel_info.append({'word': word.word, 'start': word.start, 'end': word.end})

    # Exportiere das Transkript als SRT-Datei
    srt_path = os.path.join(projekt_ordner, "geschichte_subtitles.srt")
    with open(srt_path, 'w') as file:
        for i, word_info in enumerate(wordlevel_info, start=1):
            start_time = format_srt_time(word_info['start'])
            end_time = format_srt_time(word_info['end'])
            file.write(f"{i}\n{start_time} --> {end_time}\n{word_info['word']}\n\n")

    print("\nThe subtitel saved in the project folder as \"geschichte_subtitles.srt\".")
    return srt_path
