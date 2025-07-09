:: Configuration
@echo off
SETLOCAL

set "PROJECT_DIR=."
set "VENV_DIR=%PROJECT_DIR%\venv"
set "BOT_FILE=bot.py"

:: Navigate to project directory
cd /d "%PROJECT_DIR%" || (
    echo [ERROR] Failed to find project directory
    exit /b 1
)

:: Pull latest code from GitHub
echo [INFO] Pulling latest code from GitHub...
git pull

:: Create virtual environment if not exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Virtual environment not found. Creating it...
    python -m venv "%VENV_DIR%"
)

:: Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

:: Install requirements
echo [INFO] Installing Python packages...
pip install -r requirements.txt

:: Run the bot
echo [INFO] Running bot...
python %BOT_FILE%

pause 