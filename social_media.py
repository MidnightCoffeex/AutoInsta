#***Instagram Anbindung***
from instagrapi import Client

# .txt lesen und als String speichern
def get_text_from_file(philosophie_file_path):
    with open(philosophie_file_path, 'r', encoding='utf-8') as f:
        return f.read()

def instagram_anbindung (final_clip_path, philosophie_file_path):
    cl = Client()
    cl.login('YOUR_INSTAGRAM_NAME','YOUR_INSTAGRAM_PASSWORD')

    philosophie_text_as_str = get_text_from_file(philosophie_file_path)

    cl.clip_upload(final_clip_path, philosophie_text_as_str)