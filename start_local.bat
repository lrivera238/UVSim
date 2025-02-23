@echo off
call install_python.bat

:: Refresh the environment variables
echo Refreshing environment variables...
set PATH=%PATH%;C:\Python\Scripts;C:\Python

:: Clear screen
cls

:: Restart the script to recognize Python
cmd /c start "" "%~f0"
exit

call install_pip.bat

@echo off
echo Starting Local Flask App...
echo -------------------------------------

:: Create a virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Install project dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Start Flask App
echo Starting Flask on http://127.0.0.1:5000/
start "" http://127.0.0.1:5000/  <== Opens the web app in the browser
set FLASK_APP=run.py
set FLASK_ENV=development
python run.py

:: Keep console open
pause
