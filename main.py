import speech_recognition as sr
import gtts                               # Google Text To Speech
from playsound import playsound
import os
from datetime import datetime
from notion import NotionClient

r = sr.Recognizer()
token = "secret_CKLJ5kX93Rk3L7iylNL9Xd192cCjB9FNkEw5ugzOE2I"
database_id = "0b4f862a3613498b97b5d3bb729cfb20"

client = NotionClient(token, database_id)
ACTIVATION_COMMAND = "hey sam"

def get_audio():
    with sr.Microphone() as  source:
        print("Say Something")
        audio = r.listen(source)
    return audio

def audio_to_text(audio):
    text = ""
    try:    
        text = r.recognize_google(audio)
    except sr.UnknownValueError :
        print("Speech Recognition could not understand audio")
    except sr.RequestError :
        print("could not request from API")
    return text

def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "./temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError: 
        print("could not play sound")



if __name__ == "__main__":
    while True:
        a = get_audio()
        command = audio_to_text(a)

        if ACTIVATION_COMMAND in command.lower():
            print("activate")
            # play sound
            play_sound("What can I do for you?")

            note = get_audio()
            note = audio_to_text(note)

            if note :
                play_sound(note)

                # TODO: save in NOTION
                now = datetime.now().astimezone().isoformat()
                res = client.create_page(note, now, status="Active")
                if res.status_code == 200:
                    play_sound("Stored new item")

