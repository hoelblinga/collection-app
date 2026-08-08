@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo Python wurde nicht gefunden. Siehe README.txt.
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

python server.py
pause
