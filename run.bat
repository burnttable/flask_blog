@echo off
REM Flask Blog Startup Script for Windows

echo Starting Flask Blog...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

REM Run the application
python app.py
