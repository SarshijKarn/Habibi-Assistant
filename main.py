import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import keyboard  # Import keyboard module for detecting keypress

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
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"You 🧠: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Network error.")
        return ""

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
    - Tell you the current time.
    - today's date.
    - a joke.
    - Look up information from Wikipedia.
    - Answer your questions based on my knowledge.
    - And much more!
    
    Press any key to start interacting with me.
    """
    speak(capabilities_text)
    print(capabilities_text)

# Main function
def main():
    capabilities()
    
    # Wait for user to press any key to continue
    while not keyboard.is_pressed('space'):  # Wait for space bar to be pressed
        pass
    
    speak("Let's get started!")

    while True:
        query = listen()

        if "exit" in query or "bye" in query or "stop" in query:  # Voice command to exit
            speak("Goodbye, stay safe!")
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
        elif query:
            response = habibi_bot.get_response(query)
            speak(str(response))

if __name__ == "__main__":
    main()
