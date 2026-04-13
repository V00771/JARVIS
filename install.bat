@echo off
cd /d "%~dp0"
echo ================================
echo    J.A.R.V.I.S. Installer
echo ================================
echo.

:: Pruefen ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% neq 0 (
    goto install_python
)

:: Python Version pruefen
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)

:: Pruefen ob Version zwischen 3.10 und 3.12
if "%PYMAJOR%" == "3" (
    if %PYMINOR% GEQ 10 (
        if %PYMINOR% LEQ 12 (
            echo Python %PYVER% gefunden - OK!
            goto install_libs
        )
    )
)

echo Python %PYVER% gefunden aber falsche Version!
echo Benoetigt: Python 3.10 - 3.12
echo.

:install_python
echo Installiere Python 3.12.9...
curl -o "%~dp0python_installer.exe" https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe
if %errorlevel% neq 0 (
    echo Download fehlgeschlagen! Bitte manuell installieren:
    echo https://www.python.org/downloads/release/python-3129/
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
echo Installiere JARVIS Libraries...
pip install speechrecognition pygame edge-tts groq pillow pystray pynput pyaudio
echo.
echo ================================
echo  Installation abgeschlossen!
echo  Starte jetzt autostart.vbs
echo ================================
pause