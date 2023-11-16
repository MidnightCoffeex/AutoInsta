import glob
import random
import shutil
import os
import time

from moviepy.editor import *
import tkinter as tk
from tkinter import ttk

# Neue Datenstrukturen für die Zuordnung
titel = ""
prompts = {
    "Weltallgeschichten": {
        "prompt_theme": "/Weltallgeschichten/",
        "titel_prompt": "Write me a single title for a fantasy story in a sci-fi fantasy world about dark space adventure; drama; love; the beauty of the universe; emotions; space; or other emotional stuff.\n" \
                        "Make it it emotional but also scary too in some aspect. You can put your own philosophical ideas into it if you feel like. Your output: [Title for the story]",
        "story_prompt": f"Write me a short fantasy story in a sci-fi fantasy world about dark space adventure; drama; love; the beauty of the universe; emotions; missing someone; space; or other emotional stuff. " \
                        f"Please include dialogues to enrich the narrative and character interactions, and use appropriate pauses to create the right atmosphere.  " \
                        f"The topic should be \"{titel}\". Make it emotional and heart-warming but also scary in some aspects. Feel free to incorporate your own philosophical ideas if you feel like. " \
                        f"Please provide only the story, without any additional explanations or comments, and keep it to about 125 words."

    },
    "Creepypasta": {
        "prompt_theme": "/Creepypasta/",
        "titel_prompt": "Write me a single title for a horror story in a sci-fi horror setting about eerie space adventures; suspense; terror; the unknown of the universe; fear; space; or other spine-chilling elements.\n" \
                        "Make it haunting and unnerving. You can include your own dark philosophical ideas if you feel like. Your output: [Title for the story]",
        "story_prompt": f"Write me a short horror story in a sci-fi horror setting about eerie space adventures; suspense; terror; the unknown of the universe; fear; isolation; space; or other spine-chilling elements. " \
                        f"Please include dialogues to enhance the suspense and character interactions, and use tense pauses to create an ominous atmosphere. " \
                        f"The topic should be \"{titel}\". Make it haunting and unnerving, with elements of fear and suspense. Incorporate your own dark philosophical ideas if you feel like. " \
                        f"Please provide only the story, without any additional explanations or comments, and keep it to about 125 words."
    }
}

def update_voice_dropdowns():
    # Entfernt alle bestehenden Dropdowns
    for dropdown in voice_dropdowns:
        dropdown.pack_forget()
    voice_dropdowns.clear()

    # Fügt neue Dropdowns basierend auf der Spinbox-Auswahl hinzu
    num_voices = int(spinbox.get())
    for _ in range(num_voices):
        combobox = ttk.Combobox(root, values=all_voices)
        combobox.pack(pady=5)
        voice_dropdowns.append(combobox)

def on_button_click():
    selected_voices = [dropdown.get() for dropdown in voice_dropdowns]
    print(f"Ausgewählte Stimmen für die Durchläufe: {selected_voices}")

    num_voices = len(selected_voices)
    for i, voice in enumerate(selected_voices):


        # Hier nutzt du die ausgewählten Prompts
        global prompt_theme, titel_prompt, story_prompt
        selected_theme = theme_combobox.get()
        current_prompts = prompts[selected_theme]
        prompt_theme = current_prompts["prompt_theme"]
        titel_prompt = current_prompts["titel_prompt"]
        story_prompt = current_prompts["story_prompt"]


#********************************ChatGPT********************************************+*
        from ChatGPT import chat_gpt_35, chat_gpt_storyteller, filter_valid_chars
        # Beispiel, wie man die Prompts und das Verzeichnis verwendet
        titel = chat_gpt_35(titel_prompt)
        bereinigter_titel = filter_valid_chars(titel)

    #***Ordnerstrukturen übergeben***
        # Der Projektordner basiert nun auf dem ausgewählten Thema
        theme_ordner = os.path.join("C:/Users/NightCoffe/Desktop/AutoInsta/Video/Reel", prompt_theme.strip("/"))
        music_files = glob.glob(os.path.join(theme_ordner, "music_for_autoinsta/*.mp3"))
        picture_prompts = os.path.join(theme_ordner, "picture_prompt_for_autoinsta/")

        projekt_ordner = os.path.join(theme_ordner, bereinigter_titel)
        if not os.path.exists(projekt_ordner):
            os.makedirs(projekt_ordner)

        # Ausgabe des Titels und des Projektordners
        print("Titel:", titel)
        print("Projektordner:", projekt_ordner)

        time.sleep(50)

    #***Geschichte schreiben lassen***
        geschichte = chat_gpt_storyteller(story_prompt)
        # Speichern der Geschichte in einer Textdatei im Projekt-Ordner
        story_file_path = os.path.join(projekt_ordner, "geschichte.txt")
        with open(story_file_path, "w") as file:
            file.write(geschichte)
        # Ausgabe der Geschichte
        print("\nThe Story is saved in project folder as \"geschichte.txt\".")
        print("\nPath: ", story_file_path)

        # Prompt für den philosophischen Satz und ChatGPT-Funktion aufrufen
        philosophie_prompt = f"Write a very short, philosophical sentence for the story \"{titel}\". Your output: [philosophical sentence]"
        philosophie = chat_gpt_35(philosophie_prompt)

        #Vorgefertigter Text der Hinzugefügt werden soll
        standarttext_file_path = os.path.join(theme_ordner, "standard.txt")
        with open(standarttext_file_path, "r") as file:
            standardtext = file.read()

        # Speichern des philosophischen Satzes in einer Textdatei im Projektordner
        philosophie_file_path = os.path.join(projekt_ordner, "philosophie.txt")
        with open(philosophie_file_path, "w") as file:
            file.write(philosophie+"\n"+standardtext)
        # Ausgabe des Satztes
        print(f"\nThe philosophical sentence: \"{philosophie}\" \nThe sentence is saved in the project folder as \"philosophie.txt\".")

        # Prompt für die 5 passenden Hashtags und ChatGPT-Funktion aufrufen
        hashtags_prompt = f"Write 10 suitable hashtags for the story \"{titel}\" that can build reach on Instagram and fit the theme. Your output shoul be: #[hashtag1] #[hashtag2] #[hashtag3] #[hashtag4] #[hashtag5] ..."
        hashtags = chat_gpt_35(hashtags_prompt).lower()

        # Speichern der Hashtags
        hashtags_file_path = os.path.join(projekt_ordner, "philosophie.txt")
        with open(hashtags_file_path, "a") as file:
           file.write(" "+hashtags)


        # Schreibe die Hashtags Zeilenumbruch getrennt
        # Ausgabe der Hashtags
        print(f"\nThe hashtags are: \"{hashtags}\" \nThe hashtags are saved in the project folder as \"hashtags.txt\".")
        print("\nPhilosophie Path: ", hashtags_file_path)

#*********************************Text-To-Speech*******************************
        from TextToSpeech import text_to_speech_with_elevenlabs

        # Aufrufen der Funktion text_to_speech_with_elevenlabs
        audio_path = text_to_speech_with_elevenlabs(geschichte, projekt_ordner, voice)
        print("\nAudio Path: ", audio_path)

#*******************************Transkription***********************************
        from Transkription import transcribe_audio_to_text

        # Aufrufen der Funktion transcribe_audio_to_text
        srt_path = transcribe_audio_to_text(audio_path, projekt_ordner)
        print("\nTranskript Path: ", srt_path)

#************************************Bildgeneration mit DALL-E*********************************************+
        from Bildgeneration import generate_images, calculate_number_of_images, get_audio_duration

        # Länge der Audio-Datei
        audio_duration = get_audio_duration(audio_path)
        # Zeit pro Bild in Sekunden
        time_per_image = 10
        # Anzahl der Bilder berechnen
        estimated_number_of_images = calculate_number_of_images(audio_duration, time_per_image)
        print("\nEstimated number of images:", estimated_number_of_images)

    #***Aufrufen der Funktion generate_images***
        generate_images(projekt_ordner, picture_prompts, estimated_number_of_images)

#****************************Video erstellen******************************************
        from Videoschnitt import create_video

        # Auswahl der Bilder
        image_files = glob.glob(os.path.join(projekt_ordner, "*.png"))
        image_files.sort()

        # mein Ordner mit der Hintergrund-Musik + zufällige auswahl einer .mp3-Datei mit 'volumex' die Lautstärke auf 8%
        background_music_file = random.choice(music_files)
        background_music = AudioFileClip(background_music_file).volumex(0.08)
        print("\nBackground-Music Path: ", music_files)
        create_video(image_files, audio_path, srt_path, background_music, projekt_ordner)

        #***Upload auf Sozial-Media***
        #!!!(nicht möglich, da Instagram die API als verdächtigte aktivitäten ansieht)!!!
        #from social_media import instagram_anbindung
        #instagram_anbindung(final_clip_path, philosophie_file_path)

        #***Auf Drive Hochladen***
        # Pfad zum Quellordner und zur Datei
        beitrag_file_path = os.path.join(projekt_ordner, "philosophie.txt")
        video_file_path = os.path.join(projekt_ordner, "final_video.mp4")

        # Zielordner auf dem Laufwerk G
        ziel_ordner_path = os.path.join("G:/Meine Ablage/Auto Insta/Fertige Beiträge", prompt_theme, bereinigter_titel)
        ziel_standard_path = os.path.join(ziel_ordner_path, "philosophie.txt")
        ziel_video_path = os.path.join(ziel_ordner_path, "final_video.mp4")

        # Erstellen des Zielordners, falls er nicht existiert
        if not os.path.exists(ziel_ordner_path):
            os.makedirs(ziel_ordner_path)

        # Kopieren der Dateien
        shutil.copy(beitrag_file_path, ziel_standard_path)
        shutil.copy(video_file_path, ziel_video_path)

        print(f"Durchlauf Nummer {i + 1}")


def on_theme_change(event):
    # Diese Funktion kann erweitert werden, falls zusätzliche UI-Updates nötig sind
    pass

root = tk.Tk()
root.geometry("400x600")  # Setzt die Fenstergröße auf 400x600 Pixel
root.title("Meine Anwendung")

# Stimmen die ich bei Elevenlabs gespeichert habe
voices_female = ['Bella', 'Joanne', 'Tally', 'Scarlett', 'Alice', 'Paola', 'Nicole']
voices_male = ['Ixel', 'Ixel_older', 'Jack_Smooth', 'Entity']
all_voices = voices_female + voices_male

# Hinzufügen eines Labels
label = tk.Label(root, text="Wählen Sie die Anzahl der Durchläufe:")
label.pack(pady=20)

# Hinzufügen einer Spinbox zur Auswahl der Anzahl der Durchläufe
spinbox = tk.Spinbox(root, from_=1, to=10) # Hier können Sie die Mindest- und Höchstwerte festlegen
spinbox.pack()
spinbox.bind('<Return>', lambda event: update_voice_dropdowns()) # Aktualisiert Dropdowns, wenn Enter gedrückt wird

voice_dropdowns = []

# Hinzufügen einer Dropdown-Liste für die Themen-Auswahl
theme_combobox = ttk.Combobox(root, values=list(prompts.keys()))
theme_combobox.pack(pady=5)
theme_combobox.bind("<<ComboboxSelected>>", on_theme_change)

# Hinzufügen einer Schaltfläche zur Aktualisierung der Stimmenauswahl
update_button = tk.Button(root, text="Stimmenauswahl aktualisieren", command=update_voice_dropdowns)
update_button.pack(pady=20)

# Hinzufügen einer Schaltfläche
start_button = tk.Button(root, text="Start", command=on_button_click)
start_button.pack(pady=20)

root.mainloop()
