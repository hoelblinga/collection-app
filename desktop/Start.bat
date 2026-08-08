@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo Python wurde nicht gefunden.
  echo Bitte einmalig installieren: https://www.python.org/downloads/
  echo Wichtig: beim Setup den Haken bei "Add Python to PATH" setzen.
  echo Danach diese Datei erneut per Doppelklick starten.
  echo.
  pause
  exit /b 1
)

if not exist venv (
  echo Einmalige Einrichtung, bitte kurz warten ...
  python -m venv venv
  call venv\Scripts\activate.bat
  python -m pip install --upgrade pip >nul
  pip install -r requirements.txt
) else (
  call venv\Scripts\activate.bat
)

python app.py
pause
