@echo off
echo Activating virtual environment...
call .\.venv-py311\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    echo Trying to create new virtual environment...
    python -m venv .venv-py311
    call .\.venv-py311\Scripts\activate.bat
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Installing requirements...
    pip install -r requirements.txt
)
echo Virtual environment activated successfully!
cmd /k 