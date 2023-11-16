#***ChatGPT***
import os
import openai
from API import openai_key, openai_orga
from openai import OpenAI

# Setzen Sie Ihren OpenAI-API-Schlüssel und Ihre Organisatzion ID in API.py!
#openai.organization = openai_orga()
#openai.api_key = openai_key()

client = OpenAI()

def chat_gpt_35(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def chat_gpt_storyteller(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature = 0.8,
        messages=[
            {"role": "system", "content": "You are a storyteller."},
            {"role": "assistant", "content": "Guidelines for Atmosphere, Dialogue, and Emotion:\n\n"
                                             "Expressing Emotions Through Dialogue Tags and Descriptive Sentences:\n"
                                             "Use dialogue tags and descriptive sentences to convey the emotional tone.\n"
                                             "Example: \"I never meant for it to end this way,\" he hesitated, his voice laden with sorrow.\n\n"
                                             "Using Pauses:\n"
                                             "Utilize pauses to control the flow of the dialogue and to create tension.\n"
                                             "Format pauses in seconds, for example <break time=\"0.5s\"/>."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content



def filter_valid_chars(title):
    # Filtern von unzulässigen Zeichen aus dem Titel für den Projekt_Ordner
    valid_chars = "-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    filtered_title = ''.join(c for c in title if c in valid_chars)
    return filtered_title

