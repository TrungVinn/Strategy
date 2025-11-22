#!/bin/bash

# Crypto Market Analysis Agent - Quick Start Script

echo "📊 Crypto Market Analysis Agent"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

echo "✅ Dependencies installed!"
echo ""
echo "🚀 Starting Streamlit app..."
echo "================================"
echo ""

# Run Streamlit app
streamlit run app.py
