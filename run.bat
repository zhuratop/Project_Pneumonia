@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Creating uploads directory...
if not exist uploads mkdir uploads

echo Starting the application...
python app.py

pause 