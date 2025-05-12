@echo off
setlocal enabledelayedexpansion

echo Checking Python version...
python --version 2>NUL
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.11.9 from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
if not "!PYTHON_VERSION!"=="3.11.9" (
    echo Warning: Python version !PYTHON_VERSION! detected
    echo This project is tested with Python 3.11.9
    echo Please consider installing Python 3.11.9
    echo.
    set /p CONTINUE="Do you want to continue anyway? (Y/N): "
    if /i "!CONTINUE!" neq "Y" exit /b 1
)

echo Checking Python installation...
echo Current Python executable: 
where python
echo.
echo Python version details:
python -c "import sys; print('Python executable:', sys.executable); print('Python version:', sys.version); print('Python path:', sys.path[0])"
echo.

echo Checking Docker...
docker --version >NUL 2>&1
if errorlevel 1 (
    echo Docker is not installed or not running
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
    echo Removing old virtual environment...
    rmdir /s /q venv
    if errorlevel 1 (
        echo Failed to remove old virtual environment
        echo Please close any applications that might be using it and try again
        pause
        exit /b 1
    )
)

echo Creating new virtual environment...
echo Current directory: %CD%
echo Using Python from: 
where python
echo.

REM Try to create venv with full path to Python
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_PATH=%%i
    goto :found_python
)
:found_python

echo Using Python at: !PYTHON_PATH!
echo Creating virtual environment with venv module...

python -m venv venv --clear --system-site-packages
if errorlevel 1 (
    echo Failed to create virtual environment using venv module
    echo Trying alternative method...
    
    echo Installing virtualenv package...
    python -m pip install --user virtualenv
    if errorlevel 1 (
        echo Failed to install virtualenv
        pause
        exit /b 1
    )
    
    echo Creating virtual environment using virtualenv...
    python -m virtualenv venv --clear --system-site-packages
    if errorlevel 1 (
        echo Failed to create virtual environment using virtualenv
        echo Please check:
        echo 1. You have write permissions in the current directory
        echo 2. No antivirus is blocking the operation
        echo 3. You have enough disk space
        echo.
        echo Current directory permissions:
        icacls "%CD%"
        echo.
        echo Available disk space:
        wmic logicaldisk get size,freespace,caption
        pause
        exit /b 1
    )
)

echo Verifying virtual environment structure...
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment was not created correctly
    echo Missing activation script: venv\Scripts\activate.bat
    echo.
    echo Directory contents of venv:
    dir venv /s /b
    echo.
    echo Please try:
    echo 1. Running the script as administrator
    echo 2. Disabling antivirus temporarily
    echo 3. Using a different directory with full permissions
    pause
    exit /b 1
)

echo Activating virtual environment...
set "VIRTUAL_ENV=%CD%\venv"
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment
    echo Please check if:
    echo 1. You have administrator privileges
    echo 2. No other process is using the virtual environment
    echo 3. The path to Python is correct
    echo.
    echo Current Python path:
    where python
    echo.
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Verifying activation...
python -c "import sys; print(sys.prefix)" | findstr /i "venv" >nul
if errorlevel 1 (
    echo Virtual environment was not activated correctly
    echo Please try running the script as administrator
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip --timeout 100 --retries 3 --trusted-host pypi.org --trusted-host files.pythonhosted.org
if errorlevel 1 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing requirements...
pip install -r requirements.txt --timeout 100 --retries 3 --trusted-host pypi.org --trusted-host files.pythonhosted.org
if errorlevel 1 (
    echo Failed to install requirements from primary source
    echo Trying alternative mirror...
    pip install -r requirements.txt --timeout 100 --retries 3 --index-url https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
    if errorlevel 1 (
        echo Failed to install requirements from alternative mirror
        pause
        exit /b 1
    )
)

echo Creating necessary directories...
if not exist uploads mkdir uploads
if not exist models mkdir models

echo Checking if model exists...
if not exist models\final_pneumonia_model.h5 (
    echo ERROR: Model not found in models/final_pneumonia_model.h5
    echo Please place the model file in the models directory
    pause
    exit /b 1
)

echo Building Docker image...
docker build -t pneumonia-detector .
if errorlevel 1 (
    echo Failed to build Docker image
    pause
    exit /b 1
)

echo Stopping existing container if running...
docker stop pneumonia-detector 2>nul
docker rm pneumonia-detector 2>nul

echo Starting container...
docker run -d --name pneumonia-detector ^
    -p 5000:5000 ^
    -e TF_ENABLE_ONEDNN_OPTS=0 ^
    -v "%cd%/uploads:/app/uploads" ^
    -v "%cd%/pneumonia.db:/app/pneumonia.db" ^
    -v "%cd%/models:/app/models" ^
    pneumonia-detector

if errorlevel 1 (
    echo Failed to start container
    pause
    exit /b 1
)

echo.
echo Application is running at http://localhost:5000
echo To check logs, run: docker logs pneumonia-detector
echo.
echo Press any key to show container logs...
pause
docker logs pneumonia-detector 