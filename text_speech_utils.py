from myapikeys import OPENAI_KEY
from openai import OpenAI
import sounddevice as sd
import audiofile as af
from scipy.io.wavfile import write
from gtts import gTTS

import multiprocessing
import pyttsx3
import keyboard

client = OpenAI(api_key=OPENAI_KEY)

def say(text):
		p = multiprocessing.Process(target=pyttsx3.speak, args=(text,))
		p.start()
		while p.is_alive():
			if keyboard.is_pressed('enter'):
				p.terminate()
			else:
				continue
		p.join()


def record_audio(filename, sec, sr = 44100):
    audio = sd.rec(int(sec * sr), samplerate=sr, channels=2, blocking=False)
    sd.wait()
    write(filename, sr, audio)

def record_audio_manual(filename, sr = 44100):
    input("  ** Press enter to start recording **")
    audio = sd.rec(int(10 * sr), samplerate=sr, channels=2)
    input("  ** Press enter to stop recording **")
    sd.stop()
    write(filename, sr, audio)

def play_audio(filename):
    signal, sr = af.read(filename)
    sd.play(signal, sr)

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        # New API call format
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

def translate_audio(filename):
    audio_file= open(filename, "rb")
    translation = openai.Audio.translate("whisper-1", audio_file)
    audio_file.close()
    return translation

def save_text_as_audio(text, audio_filename):
    myobj = gTTS(text=text, lang='en', slow=False)  
    myobj.save(audio_filename)



