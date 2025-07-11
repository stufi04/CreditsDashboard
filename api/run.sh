#!/bin/bash

# Exit on any error
set -e

echo "🔧 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Running the Flask app..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run