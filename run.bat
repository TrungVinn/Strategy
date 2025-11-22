@echo off
REM Crypto Market Analysis Agent - Quick Start Script (Windows)

echo 📊 Crypto Market Analysis Agent
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created!
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt

echo ✅ Dependencies installed!
echo.
echo 🚀 Starting Streamlit app...
echo ================================
echo.

REM Run Streamlit app
streamlit run app.py
