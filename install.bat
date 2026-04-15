@echo off
cd /d "%~dp0"
setlocal EnableDelayedExpansion

echo ================================
echo    J.A.R.V.I.S. Installer
echo ================================
echo.

:: === KONFIGURATION ===
set PYTHON_VERSION=3.12.9
set PYTHON_DIR=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set JARVIS_PY=jarvis.py

:: === SCHritt 1: Python 3.12 pruefen/installieren ===
:check_python
if exist "%PYTHON_EXE%" (
    echo [OK] Python 3.12 gefunden
    goto check_pip
)

echo [INFO] Python 3.12 nicht gefunden. Lade herunter...
echo.

:: Download Python 3.12.9
curl -L -o "%TEMP%\python_installer.exe" https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
if %errorlevel% neq 0 (
    echo [FEHLER] Download fehlgeschlagen!
    echo Bitte manuell installieren: https://www.python.org/downloads/release/python-3129/
    pause
    exit /b 1
)

echo [INFO] Installiere Python 3.12.9...
echo        Dies kann einen Moment dauern...

:: Installation (quiet, nur fuer diesen User, nicht in PATH)
"%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=0 TargetDir="%PYTHON_DIR%" Include_pip=1 AssociateFiles=0 Shortcuts=0

:: Cleanup
del "%TEMP%\python_installer.exe" 2>nul

:: Pruefen ob geklappt
if not exist "%PYTHON_EXE%" (
    echo [FEHLER] Python Installation fehlgeschlagen!
    pause
    exit /b 1
)

echo [OK] Python 3.12.9 installiert
echo.

:: === SCHritt 2: pip aktualisieren ===
:check_pip
echo [INFO] Aktualisiere pip...
"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel --quiet
if %errorlevel% neq 0 (
    echo [WARNUNG] pip-Update hat nicht geklappt, versuche trotzdem weiter...
)

:: === SCHritt 3: Dependencies installieren ===
:install_deps
echo.
echo [INFO] Installiere JARVIS Libraries...
echo        - speechrecognition, edge-tts, groq, pillow, pystray, pynput
echo        - pygame (dies kann eine Weile dauern)...

:: Core Libraries
"%PYTHON_EXE%" -m pip install speechrecognition edge-tts groq pillow pystray pynput --quiet
if %errorlevel% neq 0 (
    echo [FEHLER] Fehler bei Core-Libraries!
    pause
    exit /b 1
)

:: Pygame (separat wegen potenzieller Build-Zeit)
echo [INFO] Installiere pygame...
"%PYTHON_EXE%" -m pip install pygame --quiet
if %errorlevel% neq 0 (
    echo [FEHLER] pygame Installation fehlgeschlagen!
    pause
    exit /b 1
)

:: PyAudio (tricky auf Windows)
echo [INFO] Installiere PyAudio...
"%PYTHON_EXE%" -m pip install pyaudio --quiet >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] PyAudio Standard-Install fehlgeschlagen, versuche Alternative...
    "%PYTHON_EXE%" -m pip install pipwin --quiet
    "%PYTHON_EXE%" -m pipwin install pyaudio
)

echo [OK] Alle Libraries installiert

:: === SCHritt 4: JARVIS starten ===
:start_jarvis
echo.
echo ================================
echo  Installation abgeschlossen!
echo  Starte JARVIS...
echo ================================
echo.
echo TIP: Rechtsklick auf das Tray-Icon zum Beenden
echo.

:: Kurze Pause damit User lesen kann
timeout /t 2 >nul

:: Pruefen ob jarvis.py existiert
if not exist "%~dp0%JARVIS_PY%" (
    echo [FEHLER] %JARVIS_PY% nicht gefunden im Ordner: %~dp0
    echo Bitte sicherstellen dass %JARVIS_PY% im gleichen Ordner wie install.bat ist.
    pause
    exit /b 1
)

:: JARVIS starten
"%PYTHON_EXE%" "%~dp0%JARVIS_PY%"

:: Falls JARVIS abstuerzt, Fenster offenhalten
echo.
echo JARVIS wurde beendet.
pause
