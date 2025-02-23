@echo off
set PYTHON_VERSION=3.11.6
set PYTHON_INSTALLER=python-installer.exe
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

echo Checking for Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading...
    curl -o %PYTHON_INSTALLER% %PYTHON_URL%
    echo Installing Python...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
    del %PYTHON_INSTALLER%
    echo Python installation complete.
)

echo Verifying Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python installation failed.
    pause
    exit /b
)

echo Creating virtual environment...
if not exist venv (
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip and installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Starting Flask on http://127.0.0.1:5000/
start "" http://127.0.0.1:5000/  <== Opens the web app in the browser
set FLASK_APP=run.py
set FLASK_ENV=development
python run.py

echo Flask is running...
pause
