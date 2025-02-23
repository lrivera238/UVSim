:: Ensure pip is installed
python -m ensurepip --default-pip
if %errorlevel% neq 0 (
    echo ERROR: pip installation failed.
    pause
    exit /b
)
echo pip installed successfully.

:: Upgrade pip to the latest version
python -m pip install --upgrade pip