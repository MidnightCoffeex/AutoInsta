#***Bildgeneration mit DALL-E***
import os
import time

from moviepy.editor import AudioFileClip
from PIL import Image, ImageOps
import urllib.request
import glob
import random
from openai import OpenAI
client = OpenAI()

# Die Länge der Audiodatei ermitteln
def get_audio_duration(audio_path):
    audio = AudioFileClip(audio_path)
    duration_sec = audio.duration
    return duration_sec



# Die Anzahl der Bilder berechnen
def calculate_number_of_images(audio_duration, time_per_image=10):
    # Zeit pro Bild in Sekunden
    time_per_image = time_per_image

    # Berechne die geschätzte Anzahl der Bilder
    estimated_number_of_images = int(audio_duration / time_per_image) + 1
    return estimated_number_of_images

def generate_images(projekt_ordner, picture_prompts, estimated_number_of_images, max_attempts=3):
    txt_files = glob.glob(f"{picture_prompts}/*.txt")
    max_attempts_per_image = max_attempts

    for image_number in range(1, estimated_number_of_images + 1):
        attempts = 0
        success = False

        while attempts < max_attempts_per_image and not success:
            random_txt_file = random.choice(txt_files)
            with open(random_txt_file, "r") as file:
                user_prompt = file.read()

            print("\nPrompt for the generated image:\n", user_prompt)

            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=user_prompt,
                    size="1024x1792",
                    quality="hd",
                    n=1
                )
                image_url = response.data[0].url
                print("Bild URL:", image_url)
                success = True

            except openai.BadRequestError:
                print("Anfrage wurde abgelehnt. Versuche es mit einem anderen Prompt.")
                attempts += 1

            if success:
                file_name = f"image_{image_number}.png"
                image_path = os.path.join(projekt_ordner, file_name)
                download_image(image_url, image_path)


        if not success:
            print(f"Konnte kein Bild für Bild Nummer {image_number} erstellen nach {max_attempts_per_image} Versuchen.")

def download_image(image_url, image_path):
    while True:
        try:
            urllib.request.urlretrieve(image_url, image_path)
            break
        except urllib.error.ContentTooShortError:
            print("Netzwerkfehler beim Herunterladen des Bildes. Warte 5 Sekunden und versuche es erneut.")
            time.sleep(5)
