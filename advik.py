import os
import platform
import requests
import pyttsx3
import speech_recognition as sr

# 1. Setup Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 170) 

def speak(text):
    print(f"Advik: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. Setup Microphone Listener
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[🎙️ Listening... Speak now]")
        # Calibrate for background noise
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        try:
            # Listen for speech (times out after 5 seconds of silence)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            print("[⚙️ Processing speech...]")
            # Using Google's built-in speech recognition for instant results
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("[!] Didn't catch that. Please speak again.")
            return None
        except sr.RequestError:
            print("[!] Speech recognition service unavailable. Check internet connection.")
            return None

# 3. Connect to Local Ollama AI
def query_advik(prompt):
    url = "http://localhost:11434/api/generate"
    system_prompt = (
        "You are Advik, a local Jarvis-style AI assistant running on my laptop. "
        "The user will give you a command. "
        "If they ask to restart the computer, reply exactly with: [RESTART_PC] "
        "If they ask for system specs, reply exactly with: [SYSTEM_SPECS] "
        "Otherwise, reply naturally and concisely to their question."
    )
    
    payload = {
        "model": "llama3", 
        "prompt": f"{system_prompt}\nUser: {prompt}",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json().get("response", "").strip()
    except Exception as e:
        return "Connection error. Is Ollama running?"

# 4. Action Execution Engine
def execute_action(command):
    if "[RESTART_PC]" in command:
        speak("Initiating system restart sequence. Your computer will restart in 15 seconds.")
        if platform.system() == "Windows":
            os.system("shutdown /r /t 15") 
        elif platform.system() == "Linux":
            os.system("sudo reboot")
            
    elif "[SYSTEM_SPECS]" in command:
        os_info = f"{platform.system()} {platform.release()}"
        speak(f"You are currently running on a {os_info} operating system.")
        
    else:
        speak(command)

# 5. Main Program Loop
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    speak("Advik systems online and ready for voice commands.")
    
    while True:
        # Replaces text input with voice input
        user_input = listen_command()
        
        if not user_input:
            continue
        
        # Voice exit commands
        if any(word in user_input.lower() for word in ["exit", "quit", "stop", "close advik", "sleep"]):
            speak("Powering down. Goodbye, sir.")
            break
            
        ai_response = query_advik(user_input)
        execute_action(ai_response)