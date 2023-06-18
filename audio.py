# Audio module to handle TTS and STT 
# Currently not implemented

import speech_recognition as sr
import tempfile
import io
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play as pydub_play
from logger import logger

recognizer = sr.Recognizer()

def play_text(text):
    tts = gTTS(text, lang="en")
    with io.BytesIO() as f:
        tts.write_to_fp(f)
        f.seek(0)
        audio = AudioSegment.from_file(f, format="mp3")
        pydub_play(audio)
   
def listen_to_speech():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        logger.info("Recognizing...")
        text = recognizer.recognize_google(audio)
        logger.info(f"User: {text}")
        return text
    except sr.UnknownValueError:
        logger.error("Sorry, I couldn't understand what you said. Please try again.")
        return None
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None