# A python file for speech to text and other utilities
import os
import speech_recognition as sr
import urllib.request
import requests

def convert_to_text(file_path):
    """
    input:
    audio file path
    
    returns:
    text (string)
    """
    # assuming here, I get a mp3 file...
    url = file_path
    r = requests.get(url)
    with open("test.mp4", "wb") as handle:
        for data in r.iter_content():
            handle.write(data)

    command = "ffmpeg -i test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    os.system(command)
    AUDIO_FILE = "audio.wav"
    r = sr.Recognizer()

    text = ''
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
        text += r.recognize_google(audio)

    os.remove("test.mp4")
    os.remove("audio.wav")
    return text

if __name__ == "__main__":
    convert_to_text("https://cdn.fbsbx.com/v/t59.3654-21/116270940_737214636820117_5925911564562160881_n.mp4/audioclip-1595706435000-2972.mp4?_nc_cat=102&_nc_sid=7272a8&_nc_ohc=K4r8hifvq9YAX8hmohz&_nc_ht=cdn.fbsbx.com&oh=946bc42d9532e101db566a3d899d3b90&oe=5F1E7001")