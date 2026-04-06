@echo off
cd /d %~dp0
echo ================================
echo    J.A.R.V.I.S. Installer
echo ================================
echo.

:: Pruefen ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nicht gefunden. Installiere Python...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe
    python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
    del python_installer.exe
    echo Python installiert!
    echo Bitte install.bat nochmal ausfuehren!
    pause
    exit
)

echo Python gefunden!
echo.
echo Installiere JARVIS Libraries...
pip install speechrecognition pygame edge-tts groq pillow pystray pynput pyaudio
echo.
echo ================================
echo  Installation abgeschlossen!
echo  Starte jetzt autostart.vbs
echo ================================
pause