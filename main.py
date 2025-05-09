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
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import keyboard  # Import keyboard module for detecting keypress
import webbrowser  # For opening websites
import os  # For opening apps or files
import psutil  # For getting system information

# Initialize the bot
habibi_bot = ChatBot("Habibi")
trainer = ChatterBotCorpusTrainer(habibi_bot)
trainer.train("chatterbot.corpus.english")

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print(f"Habibi 🔊: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    import sounddevice as sd
    import numpy as np
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    samplerate = 44100
    duration = 5  # seconds

    print("🎙️ Listening.")
    speak("Listening.")

    try:
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        audio_data = recording.tobytes()
        audio = sr.AudioData(audio_data, samplerate, 2)

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
    now = datetime.datetime.now()
    return now.strftime("It's %I:%M %p right now.")

def get_date():
    today = datetime.date.today()
    return f"Today is {today.strftime('%B %d, %Y')}."

# Announce capabilities
def capabilities():
    capabilities_text = """
    Hello Boss, Greetings, I am Habibi, your personal assistant.
    I can:
    - Tell you the current time, date, jokes, Look up on Wikipedia, Answer your questions,
    - Play YouTube video, Open any app or file, Search the internet, and much more.
    
    Press space key to start interacting with me and say exit or bye or stop to stop.
    """
    speak(capabilities_text)
    print(capabilities_text)

# Function to search the internet
def search_internet(query):
    speak(f"Searching the internet for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to play a YouTube video
def play_youtube_video(video_name):
    speak(f"Playing {video_name} on YouTube.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={video_name}")

# Function to open an app or file
def open_app_or_file(path):
    if os.path.exists(path):
        speak(f"Opening {path}.")
        os.startfile(path)
    else:
        speak("Sorry, I couldn't find that file or application.")

# Function to get system information (example: CPU usage)
def system_info():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    speak(f"Your CPU usage is {cpu} percent and memory usage is {memory} percent.")

# Main function
def main():
    capabilities()

    # Wait for user to press any key to continue
    while not keyboard.is_pressed('space'):  # Wait for space bar to be pressed
        pass

    speak("Let's get started! Boss")

    while True:
        query = listen()

        if "exit" in query or "bye" in query or "stop" in query:  # Voice command to exit
            speak("Goodbye, stay safe, See you soon boss!")
            break

        # Stop the assistant if any key is pressed
        if keyboard.is_pressed('space'):  # Check if any key is pressed
            speak("Stopping interaction now...")
            break

        if "time" in query:
            speak(get_time())
        elif "date" in query:
            speak(get_date())
        elif "joke" in query:
            speak(pyjokes.get_joke())
        elif "what is" in query or "who is" in query or "tell me about" in query:
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
            query_to_search = query.replace("search", "").strip()
            search_internet(query_to_search)
        elif "system" in query or "cpu" in query or "memory" in query:
            system_info()
        elif query:
            response = habibi_bot.get_response(query)
            speak(str(response))

if __name__ == "__main__":
    main() 
