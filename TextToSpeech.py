#*****Text-To-Speech******
import os
import random
from elevenlabs import generate, set_api_key
from API import elevenlabs_key

# Setzen Sie Ihren elevenlabs-API-Schlüssel hier E-Mail: alenikm.business@gmail.com
set_api_key(os.environ.get("ELEVENLABS_API_KEY"))


# Good voice  'Ixel', 'Ixel_older', 'Jack_Smooth', 'Entity'
def text_to_speech_with_elevenlabs(geschichte, projekt_ordner, voice):

    audio = generate(
        text=geschichte,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    audio_path = os.path.join(projekt_ordner, "geschichte_audio.mp3")
    with open(audio_path, 'wb') as f:
        f.write(audio)
    print("\nThe story was read and the audio file was saved in the projekt_folder as geschichte_audio.mp3.")
    return audio_path
