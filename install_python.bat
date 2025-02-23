winget install --id Python.Python.3.11 -e --source winget

:: Verify installation
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python installation failed.
    pause
    exit /b
)
echo Python installed successfully.