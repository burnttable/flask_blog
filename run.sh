#!/bin/bash
# Flask Blog Startup Script for Unix/Linux/Mac

echo "Starting Flask Blog..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the application
python app.py
