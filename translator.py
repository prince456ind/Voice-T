import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os
import tempfile

recognizer = sr.Recognizer()
translator = Translator()


def speak(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        temp_file = os.path.join(tempfile.gettempdir(), "tts_temp.mp3")
        tts.save(temp_file)
        playsound(temp_file)
        try:
            os.remove(temp_file)
        except:
            pass
    except Exception as e:
        print(f"❌ Speak error: {e}")


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio, language='en-IN')
            return text
        except:
            return None


def translate_to_hindi(text):
    try:
        result = translator.translate(text, src='en', dest='hi')
        return result.text
    except Exception as e:
        print("Translation error:", e)
        return None