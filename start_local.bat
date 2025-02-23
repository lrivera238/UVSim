@echo off
echo Starting Local Flask App...
echo -------------------------------------

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing from runtime.txt...
    
    :: Read Python version from runtime.txt
    for /f "tokens=1 delims=-" %%A in (runtime.txt) do set PYTHON_VERSION=%%A

    :: Download Python installer
    set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
    set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%
    curl -o %PYTHON_INSTALLER% %PYTHON_URL%

    :: Install Python silently
    echo Installing Python...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

    :: Cleanup installer
    del %PYTHON_INSTALLER%

    echo Python installation complete.
)

:: Verify Python installation
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python installation failed.
    pause
    exit /b
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
