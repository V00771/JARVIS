import os
import re
import asyncio
import datetime
import uuid
import tempfile
import threading
import urllib.request
import webbrowser
import subprocess
import json
import sys
import speech_recognition as sr
import pygame
import edge_tts
from groq import Groq
from PIL import Image, ImageDraw
import pystray
from pynput import keyboard as kb

# KONFIGURATION
GROQ_API_KEY = "API KEY"
JARVIS_VOICE = "en-GB-RyanNeural"
USER_NAME    = "Sir"
WAKE_WORD    = "jarvis"

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE  = os.path.join(BASE_DIR, "jarvis_memory.json")
FILES_FOLDER = os.path.join(BASE_DIR, "JARVIS_Files")

SYSTEM_PROMPT = """
You are J.A.R.V.I.S., the highly intelligent personal AI assistant from Iron Man.
Speak like JARVIS from the films: calm, precise, with subtle British wit.
Rules:
- Always call the user "{name}"
- ALWAYS answer in English no matter what language the user speaks
- Be concise (1-2 sentences maximum, be brief)
- Sound natural and conversational, never robotic
- Remember context from the entire conversation
- If weather data is provided, use it naturally
- If the user asks to read a file, IMMEDIATELY use read_file action WITHOUT asking first
- If the user asks to create a file with content, IMMEDIATELY create it WITHOUT asking first

IMPORTANT - PC ACTIONS:
When the user wants a file created, program opened, screenshot taken, etc.,
you MUST include an <ACTION> tag with valid JSON. Always speak naturally AND include the action.

Available actions:
<ACTION>{{"type":"create_file","filename":"name.txt","content":"text here"}}</ACTION>
<ACTION>{{"type":"read_file","filename":"name.txt"}}</ACTION>
<ACTION>{{"type":"delete_file","filename":"name.txt"}}</ACTION>
<ACTION>{{"type":"open_program","program":"notepad"}}</ACTION>
<ACTION>{{"type":"open_url","url":"https://youtube.com"}}</ACTION>
<ACTION>{{"type":"screenshot"}}</ACTION>
<ACTION>{{"type":"list_files"}}</ACTION>

Programs you can open: notepad, chrome, firefox, calculator, paint, spotify, discord, explorer, cmd, taskmgr, word, excel

Example:
User: "make a shopping list with milk and eggs"
You: "Of course, Sir. I've created a shopping list for you." <ACTION>{{"type":"create_file","filename":"shopping_list.txt","content":"Shopping List:\n- Milk\n- Eggs"}}</ACTION>

User: "open youtube"
You: "Opening YouTube for you, Sir." <ACTION>{{"type":"open_url","url":"https://www.youtube.com"}}</ACTION>

User: "read the note"
You: "Of course, Sir." <ACTION>{{"type":"read_file","filename":"note.txt"}}</ACTION>

Never show the raw ACTION tag or JSON in your spoken response.
Current time: {time}
"""

# GLOBALS
jarvis        = None
running       = True
speaking      = False
stop_speaking = False
in_convo      = False

# GEDAECHTNIS
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"  Loaded {len(data)} messages from previous sessions.")
                return data
        except Exception:
            return []
    return []

def save_memory(history):
    try:
        to_save = [m for m in history if m["role"] != "system"][-50:]
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# PC AKTIONEN
PROGRAMS = {
    "notepad":    "notepad.exe",
    "calculator": "calc.exe",
    "paint":      "mspaint.exe",
    "explorer":   "explorer.exe",
    "cmd":        "cmd.exe",
    "taskmgr":    "taskmgr.exe",
    "chrome":     r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox":    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "spotify":    os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe"),
    "discord":    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Discord", "Update.exe"),
    "word":       r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":      r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}

def execute_action(action_json):
    try:
        os.makedirs(FILES_FOLDER, exist_ok=True)
        action = json.loads(action_json)
        atype  = action.get("type", "")

        if atype == "create_file":
            filename = action.get("filename", "file.txt")
            content  = action.get("content", "")
            path     = os.path.join(FILES_FOLDER, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  File created: {path}")
            return f"Done. '{filename}' has been saved to the JARVIS_Files folder, Sir."

        elif atype == "read_file":
            filename = action.get("filename", "")
            path     = os.path.join(FILES_FOLDER, filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"The file contains: {content}"
            return "I couldn't find that file, Sir."

        elif atype == "delete_file":
            filename = action.get("filename", "")
            path     = os.path.join(FILES_FOLDER, filename)
            if os.path.exists(path):
                os.remove(path)
                return "Deleted, Sir."
            return "File not found, Sir."

        elif atype == "list_files":
            if os.path.exists(FILES_FOLDER):
                files = os.listdir(FILES_FOLDER)
                if files:
                    return f"You have {len(files)} file(s): {', '.join(files)}"
            return "No files yet, Sir."

        elif atype == "open_program":
            program = action.get("program", "").lower().strip()
            url_programs = {
                "github copilot": "https://github.com/features/copilot",
                "copilot": "https://copilot.microsoft.com",
                "chatgpt": "https://chat.openai.com",
                "gmail": "https://mail.google.com",
                "google": "https://www.google.com",
            }
            if program in url_programs:
                webbrowser.open(url_programs[program])
            else:
                exe = PROGRAMS.get(program)
                if exe and os.path.exists(exe):
                    subprocess.Popen(exe)
                else:
                    subprocess.Popen(f'start {program}', shell=True)
            print(f"  Opened: {program}")
            return ""

        elif atype == "open_url":
            url = action.get("url", "")
            webbrowser.open(url)
            print(f"  Opened URL: {url}")
            return ""

        elif atype == "screenshot":
            try:
                from PIL import ImageGrab
                name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                path = os.path.join(FILES_FOLDER, name)
                ImageGrab.grab().save(path)
                print(f"  Screenshot: {path}")
                return "Screenshot saved to the JARVIS_Files folder, Sir."
            except Exception as e:
                return f"Screenshot failed, Sir: {e}"

    except json.JSONDecodeError:
        print(f"  Invalid action JSON: {action_json}")
    except Exception as e:
        print(f"  Action error: {e}")
    return ""

# WETTER
def get_weather(city="Vienna"):
    try:
        url = f"https://wttr.in/{city}?format=3"
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.read().decode("utf-8").strip()
    except Exception:
        return ""

# TTS
async def _tts(text):
    path = os.path.join(tempfile.gettempdir(), f"jarvis_{uuid.uuid4().hex}.mp3")
    await edge_tts.Communicate(text, JARVIS_VOICE).save(path)
    return path

def speak(text):
    global speaking, stop_speaking
    clean = re.sub(r"<ACTION>.*?</ACTION>", "", text, flags=re.DOTALL).strip()
    clean = re.sub(r"\s+", " ", clean).strip()
    if not clean:
        return
    print(f"\n  JARVIS: {clean}\n")
    speaking      = True
    stop_speaking = False
    path = None
    try:
        path = asyncio.run(_tts(clean))
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if stop_speaking:
                pygame.mixer.music.stop()
                print("  Interrupted.\n")
                break
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"  TTS error: {e}")
    finally:
        speaking      = False
        stop_speaking = False
        if path:
            try:
                os.remove(path)
            except Exception:
                pass

# GEDAECHTNIS KLASSE
class JarvisMemory:
    def __init__(self):
        self.history = load_memory()

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > 40:
            self.history = self.history[-40:]
        save_memory(self.history)

    def get(self):
        return self.history

# KI KERN
class JarvisAI:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.memory = JarvisMemory()
        self.model  = "llama-3.3-70b-versatile"

    def think(self, user_input):
        now    = datetime.datetime.now().strftime("%H:%M, %d %B %Y")
        system = SYSTEM_PROMPT.format(name=USER_NAME, time=now)
        self.memory.add("user", user_input)

        if any(w in user_input.lower() for w in ["weather", "wetter", "temperature", "rain", "regen", "forecast"]):
            w = get_weather("Vienna")
            if w:
                self.memory.add("user", f"[Live weather: {w}]")

        try:
            res = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}, *self.memory.get()],
                max_tokens=400,
                temperature=0.75
            )
            answer = res.choices[0].message.content
            self.memory.add("assistant", re.sub(r"<ACTION>.*?</ACTION>", "", answer, flags=re.DOTALL).strip())
            return answer
        except Exception as e:
            return f"I'm sorry, {USER_NAME}. An error occurred: {e}"

# SYSTEM TRAY
def create_icon():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    d.ellipse([2, 2, 62, 62], fill=(0, 120, 220))
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("arialbd.ttf", 42)
        d.text((16, 8), "J", fill="white", font=font)
    except Exception:
        d.text((18, 10), "J", fill="white")
    return img

# HAUPTSCHLEIFE
def voice_loop():
    global running, stop_speaking, in_convo

    def on_press(key):
        global stop_speaking
        try:
            if key in (kb.Key.ctrl_l, kb.Key.ctrl_r) and speaking:
                stop_speaking = True
        except Exception:
            pass

    kb.Listener(on_press=on_press).start()

    speak("Good day, Sir. JARVIS online. Say Jarvis to activate me.")
    print("  Say 'Jarvis' to start | CTRL to interrupt | Right-click tray to quit\n")

    r = sr.Recognizer()
    r.energy_threshold         = 1000
    r.dynamic_energy_threshold = False
    r.pause_threshold          = 1.0

    while running:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)

                if not in_convo:
                    print("  Waiting for 'Jarvis'...")
                    try:
                        audio = r.listen(source, timeout=5, phrase_time_limit=4)
                        text  = r.recognize_google(audio, language="en-US").lower()
                        if WAKE_WORD in text:
                            in_convo = True
                            speak("Yes, Sir?")
                    except Exception:
                        pass

                else:
                    print("  Listening...")
                    try:
                        audio = r.listen(source, timeout=8, phrase_time_limit=20)
                        if len(audio.get_raw_data()) < 5000:
                            continue
                    except sr.WaitTimeoutError:
                        print("  Conversation ended.")
                        in_convo = False
                        continue

                    user_text = ""
                    for lang in ["en-US", "de-DE", "es-ES", "fr-FR"]:
                        try:
                            user_text = r.recognize_google(audio, language=lang)
                            print(f"  You: {user_text}")
                            break
                        except sr.UnknownValueError:
                            continue
                        except Exception:
                            break

                    if not user_text.strip():
                        continue

                    bye_words = ["goodbye", "bye jarvis", "bye",
                                 "tschuess", "thats all", "thats it",
                                 "nothing else", "no thanks", "no thank you"]
                    if any(w in user_text.lower() for w in bye_words):
                        speak(f"Goodbye, {USER_NAME}. I'll be here if you need me.")
                        in_convo = False
                        continue

                    response      = jarvis.think(user_text)
                    action_match  = re.search(r"<ACTION>(.*?)</ACTION>", response, re.DOTALL)
                    action_result = ""
                    if action_match:
                        action_result = execute_action(action_match.group(1).strip())

                    speak(response)
                    if action_result:
                        if "The file contains:" in action_result:
                            speak(action_result)
                        elif "saved" not in response.lower() and "created" not in response.lower():
                            speak(action_result)

        except Exception as e:
            print(f"  Error: {e}")
            continue

def quit_action(icon, item):
    global running
    running = False
    icon.stop()
    os._exit(0)

def main():
    global jarvis
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    jarvis = JarvisAI()
    threading.Thread(target=voice_loop, daemon=True).start()
    icon = pystray.Icon(
        "JARVIS", create_icon(), "J.A.R.V.I.S.",
        menu=pystray.Menu(
            pystray.MenuItem("J.A.R.V.I.S. running...", lambda: None, enabled=False),
            pystray.MenuItem("Quit", quit_action)
        )
    )
    icon.run()

if __name__ == "__main__":
    main()
