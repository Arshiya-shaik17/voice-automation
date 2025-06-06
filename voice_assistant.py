import speech_recognition as sr
import pyttsx3
import subprocess
import platform
import os
import sys

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Configure TTS voice properties
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_command():
    """Listen for voice command and return recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, there seems to be a network error.")
        return ""

def open_application(app_name):
    """Open applications based on OS."""
    system = platform.system()
    if system == "Windows":
        apps = {
            "calculator": "calc.exe",
            "notepad": "notepad.exe",
            "command prompt": "cmd.exe"
        }
        if app_name in apps:
            subprocess.Popen(apps[app_name])
            speak(f"Opening {app_name}")
        else:
            speak(f"Sorry, I can't open {app_name}")
    elif system == "Darwin":  # macOS
        apps = {
            "calculator": "open -a Calculator",
            "textedit": "open -a TextEdit",
            "terminal": "open -a Terminal"
        }
        if app_name in apps:
            os.system(apps[app_name])
            speak(f"Opening {app_name}")
        else:
            speak(f"Sorry, I can't open {app_name}")
    else:
        speak("Sorry, your operating system is not supported for opening apps.")

def run_script(script_path):
    """Run a python script."""
    try:
        subprocess.Popen([sys.executable, script_path])
        speak(f"Running script {os.path.basename(script_path)}")
    except Exception as e:
        speak(f"Failed to run script: {e}")

def handle_command(command):
    """Dispatch voice command to appropriate action."""
    if "open calculator" in command:
        open_application("calculator")
    elif "open notepad" in command:
        open_application("notepad")
    elif "open command prompt" in command:
        open_application("command prompt")
    elif "run backup script" in command:
        # Change to your actual script path
        run_script("backup_script.py")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        sys.exit()
    else:
        speak("Sorry, I don't know that command.")

def main():
    speak("Voice assistant started. How can I help you?")
    while True:
        command = listen_command()
        if command:
            handle_command(command)

if __name__ == "__main__":
    main()
