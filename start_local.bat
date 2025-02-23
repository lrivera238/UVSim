@echo off
echo Starting Local Flask App...
echo -------------------------------------

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing using winget...

    :: Install Python using winget
    winget install --id Python.Python.3.11 -e --source winget

    :: Verify installation
    python --version
    if %errorlevel% neq 0 (
        echo ERROR: Python installation failed.
        pause
        exit /b
    )
    echo Python installed successfully.
)

:: Create a virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Upgrade pip and install requirements
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Start Flask App
echo Starting Flask on http://127.0.0.1:5000/
start "" http://127.0.0.1:5000/  <== Opens the web app in the browser
set FLASK_APP=run.py
set FLASK_ENV=development
python run.py

:: Keep console open
pause
