# J.A.R.V.I.S. - Personal AI Assistant

> *"Good day, Sir. JARVIS online."*  
> A voice-controlled AI assistant inspired by Iron Man's J.A.R.V.I.S., running locally on your PC.

---

## ⚠️ Important – Before You Start

### Disable Smart App Control (Windows 11 only)
Windows 11's **Smart App Control** may block JARVIS from running.  
You **must** disable it before starting:

1. Open **Windows Security** (search in Start Menu)
2. Click **App & browser control**
3. Click **Smart App Control settings**
4. Set it to **Off**

> ⚠️ Windows will warn you – this is normal. Smart App Control can be turned back on anytime.  
> Without disabling it, JARVIS may be blocked from starting.

---

## 🚀 Quick Start

### Step 1 – Download
Download these files and put them all in the **same folder**:
- `jarvis.pyw`
- `install.bat`
- `start_jarvis.bat`
- `autostart.vbs`

### Step 2 – Install
Double-click **`install.bat`**  
This will automatically:
- ✅ Check if Python 3.10–3.12 is installed (installs 3.12.9 if not)
- ✅ Install all required libraries
- ✅ Takes about 2–5 minutes on first run

### Step 3 – Start JARVIS
Choose one of two options:

| File | Description |
|---|---|
| `start_jarvis.bat` | Starts JARVIS **with** a console window (good for debugging) |
| `autostart.vbs` | Starts JARVIS **without** any window (clean, recommended) |

Double-click either file to start. A **blue "J" icon** will appear in your system tray (bottom right).

---

## 🎤 How to Use

1. Say **"Jarvis"** to wake him up
2. Ask anything or give a command
3. Say **"bye"** or **"goodbye"** to end the conversation
4. **Right-click** the tray icon → **Quit** to close JARVIS

---

## 🗣️ Voice Commands

### General
| Say | Action |
|---|---|
| *"What's the weather?"* | Live weather for Vienna |
| *"What time is it?"* | Current time |
| *"Open YouTube"* | Opens YouTube in browser |
| *"Open Chrome"* | Opens Chrome |
| *"Open Spotify"* | Opens Spotify |

### Files
| Say | Action |
|---|---|
| *"Make a note with..."* | Creates a text file |
| *"Read the note"* | Reads file out loud |
| *"List my files"* | Lists all saved files |
| *"Delete the note"* | Deletes a file |
| *"Take a screenshot"* | Saves screenshot |

### Conversation
| Say | Action |
|---|---|
| *"bye"* / *"goodbye"* | Ends conversation |
| *"nothing else"* | Ends conversation |
| *"no thanks"* | Ends conversation |

> 💡 JARVIS understands **English, German, Spanish and French**

---

## ⌨️ Keyboard Shortcut
| Key | Action |
|---|---|
| `CTRL` | Interrupt JARVIS while he is speaking |

---

## 📁 Files Explained

| File | Description | Download needed? |
|---|---|---|
| `jarvis.pyw` | Main program | ✅ Yes |
| `install.bat` | Installer | ✅ Yes |
| `start_jarvis.bat` | Start with console | ✅ Yes |
| `autostart.vbs` | Start without console | ✅ Yes |
| `jarvis_memory.json` | Conversation memory | ❌ No – created automatically |
| `JARVIS_Files/` | Folder for created files | ❌ No – created automatically |

---

## 💻 System Requirements

| | Minimum |
|---|---|
| OS | Windows 10 / 11 |
| Python | 3.10 – 3.12 (installed automatically) |
| RAM | 4 GB |
| Internet | Required (speech recognition + AI) |
| Microphone | Required |

---

## ❓ Troubleshooting

**JARVIS doesn't hear me**
- Check if your microphone is set as default in Windows sound settings
- Make sure no other app is using the microphone

**"No module named..." error**
- Run `install.bat` again

**JARVIS speaks but doesn't react to "Jarvis"**
- Speak clearly and say just *"Jarvis"*
- Check your microphone volume in Windows settings

**Tray icon doesn't appear**
- Run `start_jarvis.bat` instead to see error messages in the console

**JARVIS is blocked / won't start**
- Disable Smart App Control (see top of this README)

---

## 🔑 API Key
This project uses the **Groq API** for AI responses.  
The API key is included – no setup needed.

---

*Made with ❤️ inspired by Tony Stark*
