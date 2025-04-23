# Habibi Assistant

**Habibi Assistant** is a voice-controlled personal assistant built using Python. It offers multiple functionalities, including time and date checking, web searches, playing YouTube videos, opening apps or files, providing system information, and answering questions based on pre-trained knowledge. This assistant utilizes voice recognition and text-to-speech capabilities to interact with the user.

## Features

- **Time & Date**: Ask for the current time or date.
- **Jokes**: Get random jokes for some light-hearted moments.
- **Wikipedia**: Ask about any topic, and the assistant will fetch a brief summary from Wikipedia.
- **YouTube**: Play a video by searching its name on YouTube.
- **Open Apps & Files**: Open any application or file on your system by providing its path.
- **Internet Search**: Search any query directly on Google.
- **System Info**: Get the current system CPU and memory usage.

## Requirements

Ensure you have Python 3.6+ installed. You will need the following libraries:

- `speechrecognition` for voice input.
- `pyttsx3` for text-to-speech output.
- `wikipedia` for fetching summaries from Wikipedia.
- `pyjokes` for generating jokes.
- `chatterbot` for conversational AI features.
- `keyboard` for detecting keypresses.
- `webbrowser` for searching the internet and opening URLs.
- `os` for opening files and applications.
- `psutil` for system information.

### Install required libraries:

You can install the necessary libraries with pip:

```bash
pip install speechrecognition pyttsx3 wikipedia pyjokes chatterbot keyboard psutil

python main.py
