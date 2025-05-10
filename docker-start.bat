@echo off
echo Stopping and removing existing container if exists...
docker stop pneumonia-detector 2>nul
docker rm pneumonia-detector 2>nul

echo Building Docker image...
docker build -t pneumonia-detector .

echo Creating uploads directory if not exists...
if not exist uploads mkdir uploads

echo Starting container...
docker run -d --name pneumonia-detector ^
    -p 5000:5000 ^
    -e TF_ENABLE_ONEDNN_OPTS=0 ^
    -v "%cd%/uploads:/app/uploads" ^
    -v "%cd%/pneumonia.db:/app/pneumonia.db" ^
    pneumonia-detector

echo.
echo Application is running at http://localhost:5000 