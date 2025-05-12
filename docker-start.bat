@echo off
echo Stopping and removing existing container if exists...
docker stop pneumonia-detector 2>nul
docker rm pneumonia-detector 2>nul

echo Creating necessary directories...
if not exist uploads mkdir uploads
if not exist models mkdir models

echo Checking if model exists...
if not exist models\final_pneumonia_model.h5 (
    echo ERROR: Model not found in models/final_pneumonia_model.h5
    echo Please place the model file in the models directory
    exit /b 1
)

echo Building Docker image...
docker build -t pneumonia-detector .

echo Starting container...
docker run -d --name pneumonia-detector ^
    -p 5000:5000 ^
    -e TF_ENABLE_ONEDNN_OPTS=0 ^
    -v "%cd%/uploads:/app/uploads" ^
    -v "%cd%/pneumonia.db:/app/pneumonia.db" ^
    -v "%cd%/models:/app/models" ^
    pneumonia-detector

echo.
echo Application is running at http://localhost:5000
echo To check logs, run: docker logs pneumonia-detector
echo.
echo Press any key to show container logs...
pause
docker logs pneumonia-detector 