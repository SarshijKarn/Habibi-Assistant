instructions = r"""
Step 1: Create a virtual environment  
Command: python -m venv venv

Step 2: Activate the virtual environment  
For Windows:  
Command: venv\\Scripts\\activate  
For macOS/Linux:  
Command: source venv/bin/activate
 
Step 3: Upgrade pip to the latest version  
Command: pip install --upgrade pip

Step 4: Install the required dependencies  
Command: pip install -r requirements.txt

Additional dependencies (use compatible versions to avoid errors):  
Command: pip install numpy==1.24.4 h5py==3.10.0 spacy

Step 5: Run the main Python script  
Command: python main.py
"""

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import keyboard
import webbrowser
import os
import psutil
import openai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import subprocess

# OpenAI API setup
openai.api_key = "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"

# Get response from OpenAI LLM
def get_llm_response(prompt):
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error generating response: {e}"

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print(f"Habibi 🔊: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    print("🎙️ Listening.")
    speak("Listening.")

    try:
        duration = 5  # seconds
        samplerate = 16000
        print("🎙️ Recording audio using sounddevice...")
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav.write(f.name, samplerate, recording)
            with sr.AudioFile(f.name) as source:
                audio = recognizer.record(source)

        print("⌛ Recognizing.")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"✅ You said: {query}")

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand.")
        query = ""
    except sr.RequestError:
        print("❌ Could not request results from Google Speech Recognition.")
        query = ""
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        query = ""

    return query

def get_time():
    return datetime.datetime.now().strftime("It's %I:%M %p right now.")

def get_date():
    return f"Today is {datetime.date.today().strftime('%B %d, %Y')}."

# Announce capabilities
def capabilities():
    text = """
    Hello Boss, Greetings, I am Habibi, your personal assistant.
    I can:
    - Tell you the current time, date, jokes, Look up on Wikipedia, Answer your questions,
    - Play YouTube video, Open any app or file, Search the internet, and much more.
    Press space key to start interacting with me and say exit or bye or stop to stop.
    """
    speak(text)
    print(text)

def search_internet(query):
    speak(f"Searching the internet for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def play_youtube_video(video_name):
    speak(f"Playing {video_name} on YouTube.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={video_name}")

def open_app_or_file(path):
    if os.path.exists(path):
        speak(f"Opening {path}.")
        os.startfile(path)
    else:
        speak("Sorry, I couldn't find that file or application.")

def system_info():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    speak(f"Your CPU usage is {cpu} percent and memory usage is {memory} percent.")

def main():
    capabilities()

    # Wait for user to press space bar to start
    while not keyboard.is_pressed('space'):
        pass

    speak("Let's get started! Boss")

    while True:
        query = listen().lower()

        if any(word in query for word in ["exit", "bye", "stop"]):
            speak("Goodbye, stay safe, See you soon boss!")
            break

        if keyboard.is_pressed('space'):
            speak("Stopping interaction now...")
            break

        if "time" in query:
            speak(get_time())
        elif "date" in query:
            speak(get_date())
        elif "joke" in query:
            speak(pyjokes.get_joke())
        elif any(kw in query for kw in ["what is", "who is", "tell me about"]):
            try:
                topic = query.replace("what is", "").replace("who is", "").replace("tell me about", "").strip()
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except Exception:
                speak("Couldn't find that on Wikipedia.")
        elif "play" in query and "youtube" in query:
            video_name = query.replace("play", "").replace("youtube", "").strip()
            play_youtube_video(video_name)
        elif "open" in query:
            path = query.replace("open", "").strip()
            open_app_or_file(path)
        elif "search" in query:
            search_internet(query.replace("search", "").strip())
        elif any(word in query for word in ["system", "cpu", "memory"]):
            system_info()
        elif query:
            speak(get_llm_response(query))

if __name__ == "__main__":
    main()
