@echo off
cd /d "%~dp0"
echo ================================
echo    J.A.R.V.I.S. Installer
echo ================================
echo.

:: Pruefen ob Python 3.12 installiert ist
py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python 3.12 gefunden!
    set PYTHON_CMD=py -3.12
    goto install_libs
)

:: Alternative: python3.12 oder python pruefen
python --version 2>&1 | findstr "3.12" >nul
if %errorlevel% equ 0 (
    echo Python 3.12 gefunden!
    set PYTHON_CMD=python
    goto install_libs
)

echo Python 3.12 nicht gefunden!
goto install_python

:install_python
echo Installiere Python 3.12.9...
curl -o "%~dp0python_installer.exe" https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe 
if %errorlevel% neq 0 (
    echo Download fehlgeschlagen! Bitte manuell installieren.
    pause
    exit
)
"%~dp0python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
del "%~dp0python_installer.exe"
echo Python 3.12.9 installiert!
echo Bitte install.bat nochmal ausfuehren!
pause
exit

:install_libs
echo.

echo Aktualisiere pip...
%PYTHON_CMD% -m pip install --upgrade pip

echo Installiere JARVIS Libraries...
%PYTHON_CMD% -m pip install speechrecognition pygame edge-tts groq pillow pystray pynput

:: PyAudio separat
echo Installiere PyAudio...
%PYTHON_CMD% -m pip install pyaudio >nul 2>&1
if %errorlevel% neq 0 (
    echo PyAudio pip-Install fehlgeschlagen, versuche Pre-Built Wheel...
    %PYTHON_CMD% -m pip install pipwin
    %PYTHON_CMD% -m pipwin install pyaudio
)

echo.
echo ================================
echo  Installation abgeschlossen!
echo  JARVIS wird jetzt gestartet...
echo ================================
timeout /t 2 >nul

start "" wscript "%~dp0autostart.vbs"
