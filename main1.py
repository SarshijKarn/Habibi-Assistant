import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import keyboard  # Import keyboard module for detecting keypress
import webbrowser  # For opening websites
import os  # For opening apps or files
import psutil  # For getting system information
import openai

openai.api_key = "your-api-key-here"  # Replace with your OpenAI API key

def get_llm_response(prompt):
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # Replace with the desired model
            prompt=prompt,
            max_tokens=150  # Set an appropriate max_tokens value
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error generating response: {e}"

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print(f"Habibi 🔊: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    samplerate = 44100
    duration = 5  # seconds

    print("🎙️ Listening.")
    speak("Listening.")

    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
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

    while True:
        # Wait for user to press space key to continue or proceed
        while not keyboard.is_pressed('space'):
            pass  # Wait for the spacebar to be pressed

        speak("Let's get started! Boss")

        query = listen()  # Listen for input after spacebar press

        if "exit" in query or "bye" in query or "stop" in query:  # Voice command to exit
            speak("Goodbye, stay safe, See you soon boss!")
            break

        # Skip the speaking and go straight to input processing if space is pressed
        if keyboard.is_pressed('space'):
            speak("Skipping speech. Let's get input.")

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
            response = get_llm_response(query)
            speak(response)

if __name__ == "__main__":
    main()
