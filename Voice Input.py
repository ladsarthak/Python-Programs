import time
import sys
import threading
import random

# 🎨 Lazy color setup
def init_colors():
    from colorama import Fore, Style, init
    init(autoreset=True)
    return Fore, Style

Fore, Style = init_colors()

# 🎤 Voice engine init (lazy import)
def init_tts():
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    return engine

tts = init_tts()

# Control for idle "alive" effect
idle_running = False
idle_thread = None

# 🎵 Boot sound (lazy import)
def boot_sound(duration=1.5):
    import numpy as np
    import sounddevice as sd
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    main_wave = 0.5 * np.sin(2 * np.pi * np.linspace(220, 880, len(t)) * t)
    bg_wave = 0.15 * np.sin(2 * np.pi * np.linspace(1200, 2000, len(t)) * t)
    wave = main_wave + bg_wave
    fade_in = np.linspace(0,1,int(fs*0.3))
    fade_out = np.linspace(1,0,int(fs*0.3))
    wave[:len(fade_in)] *= fade_in
    wave[-len(fade_out):] *= fade_out
    sd.play(wave, fs)
    sd.wait()

# 🎵 Shutdown sound (lazy import)
def shutdown_sound(duration=1.5):
    import numpy as np
    import sounddevice as sd
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    main_wave = 0.5 * np.sin(2 * np.pi * np.linspace(880, 220, len(t)) * t)
    bg_wave = 0.15 * np.sin(2 * np.pi * np.linspace(2000, 1200, len(t)) * t)
    wave = main_wave + bg_wave
    fade_out = np.linspace(1,0,int(fs*0.5))
    wave[-len(fade_out):] *= fade_out
    sd.play(wave, fs)
    sd.wait()

# 🔹 Idle alive effect (tiny soft pings at random intervals)
def idle_effect():
    global idle_running
    import numpy as np
    import sounddevice as sd
    fs = 44100
    while idle_running:
        duration = 0.2
        t = np.linspace(0, duration, int(fs*duration), endpoint=False)
        freq = random.uniform(1300, 1800)
        wave = 0.02 * np.sin(2 * np.pi * freq * t)
        sd.play(wave, fs)
        sd.wait()
        time.sleep(random.uniform(3,6))

# 💫 Boot sequence animation with glowy loading bar + boot sound at the end
def boot_sequence():
    import time
    import sys

    # Steps for the loading bar
    steps = ["Activating voice recognition module...",
             "Loading conversational protocols...",
             "Engaging idle subroutines...",
             "Finalizing system checks..."]

    print(Fore.CYAN + "Initializing J.A.R.V.I.S. Systems...\n")

    for step in steps:
        total = 20  # length of bar
        for j in range(total + 1):
            percent = int((j / total) * 100)
            bar = Fore.GREEN + "▓" * j + Fore.WHITE + "░" * (total - j)
            sys.stdout.write(f"\r{step} [{bar}] {percent}%")
            sys.stdout.flush()
            time.sleep(0.05)
        print()  # new line after each step
        time.sleep(0.3)

    # Play the cinematic boot sound AFTER all bars
    try:
        boot_sound()
    except Exception as e:
        print(Fore.RED + f"⚠️ Could not play boot sound: {e}")

    print(Fore.GREEN + Style.BRIGHT + "\n✅ J.A.R.V.I.S. online. Awaiting activation phrase: 'Hey Jarvis'.\n")

# 🗣️ Speak function
def speak(text):
    print(Fore.YELLOW + "J.A.R.V.I.S.:" + Style.RESET_ALL, text)
    tts.say(text)
    tts.runAndWait()

# 🎤 Listen function (lazy import)
def listen():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            print(Fore.CYAN + "Heard:" + Fore.WHITE, text)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network interface unavailable, sir.")
            return ""

# 🌐 Browser search function (lazy import)
def browser_search(query):
    import webbrowser
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)
    speak(f"I've opened the search results for {query}, sir.")

# 💬 Chatbot responses
def get_bot_response(message):
    message = message.lower()
    if "hello" in message or "hi" in message:
        return "Good day, sir. How may I assist you?"
    elif "your name" in message:
        return "I am J.A.R.V.I.S., Just A Rather Very Intelligent System, at your service."
    elif "time" in message:
        import time as t
        return "It is currently " + t.strftime("%I:%M %p")
    elif "date" in message:
        import time as t
        return "Today's date is " + t.strftime("%B %d, %Y")
    elif "system status" in message:
        return "All systems are running at peak efficiency, sir."
    elif "who made you" in message:
        return "You did, sir. I exist because of your brilliance."
    elif "self destruct" in message:
        return "I’m afraid I can’t do that, sir. My safety protocols forbid it."
    elif "shutdown" in message:
        return "Understood. Powering down systems."
    elif "thank you" in message:
        return "Always a pleasure, sir."
    else:
        return None  # unknown command, maybe browser search

# 🚀 Boot JARVIS
boot_sequence()

# 🔹 Map of keywords to websites
website_map = {
    "youtube": "https://www.youtube.com",
    "lichess": "https://lichess.org",
    "twitter": "https://twitter.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    # add more sites as needed
}

while True:
    heard = listen()

    if "hey jarvis" in heard:
        idle_running = True
        idle_thread = threading.Thread(target=idle_effect)
        idle_thread.start()

        speak("Online and ready, sir. What shall I do first?")

        while True:
            user_input = listen()
            if not user_input:
                continue

            # Sleep mode
            if "stop listening" in user_input or "standby" in user_input:
                speak("Understood, entering standby mode.")
                idle_running = False
                if idle_thread:
                    idle_thread.join()
                break

            # Exit mode
            if "exit" in user_input or "power down" in user_input:
                speak("Commencing full shutdown. Goodbye, sir.")
                idle_running = False
                if idle_thread:
                    idle_thread.join()
                try:
                    shutdown_sound()
                except Exception as e:
                    print(Fore.RED + f"⚠️ Could not play shutdown sound: {e}")
                sys.exit()

            # Open website if user says "open <site>"
            if user_input.startswith("open "):
                site_name = user_input.replace("open ", "").strip().lower()
                url = website_map.get(site_name)
                if url:
                    import webbrowser
                    webbrowser.open(url)
                    speak(f"Opening {site_name}, sir.")
                else:
                    speak(f"I don’t have a URL for {site_name}, sir.")
                continue

            # Browser search if first word is 'search'
            if user_input.split()[0] == "search":
                query = " ".join(user_input.split()[1:]).strip()
                if query:
                    browser_search(query)
                else:
                    speak("Please provide a search query, sir.")
                continue

            # Normal chatbot responses
            response = get_bot_response(user_input)
            if response:
                speak(response)
            else:
                speak("Command not recognized, sir. Perhaps you want me to search the web?")
