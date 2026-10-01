import os
import platform
import requests
import pyttsx3

# 1. Setup Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Try to set a clear English voice (0 is usually male, 1 is usually female on Windows)
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 170) # Speed of speech

def speak(text):
    print(f"Advik: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. Connect to Local Ollama AI
def query_advik(prompt):
    url = "http://localhost:11434/api/generate"
    # This prompt tells the AI how to act and when to trigger system commands
    system_prompt = (
        "You are Advik, a local Jarvis-style AI assistant running on my laptop. "
        "The user will give you a command. "
        "If they ask to restart the computer, reply exactly with: [RESTART_PC] "
        "If they ask for system specs, reply exactly with: [SYSTEM_SPECS] "
        "Otherwise, reply naturally and concisely to their question."
    )
    
    payload = {
        "model": "llama3", # Make sure you have pulled this model in Ollama
        "prompt": f"{system_prompt}\nUser: {prompt}",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json().get("response", "").strip()
    except Exception as e:
        return "Connection error. Make sure the Ollama app is running in the background."

# 3. Action Execution Engine
def execute_action(command):
    if "[RESTART_PC]" in command:
        speak("Initiating system restart sequence. Your computer will restart in 15 seconds.")
        # Windows restart command (15 second delay so you can cancel it if needed)
        if platform.system() == "Windows":
            os.system("shutdown /r /t 15") 
        elif platform.system() == "Linux":
            os.system("sudo reboot")
            
    elif "[SYSTEM_SPECS]" in command:
        os_info = f"{platform.system()} {platform.release()}"
        speak(f"You are currently running on a {os_info} operating system.")
        
    else:
        # Just speak the normal conversational reply
        speak(command)

# 4. Main Program Loop
if __name__ == "__main__":
    # Clear the terminal screen for a clean look
    os.system("cls" if os.name == "nt" else "clear")
    speak("Advik systems online and ready.")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "stop", "close"]:
            speak("Powering down. Goodbye.")
            break
            
        ai_response = query_advik(user_input)
        execute_action(ai_response)