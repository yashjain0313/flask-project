#!/bin/bash

# Flask Task Manager Setup Script

echo "🚀 Setting up Flask Task Manager..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create environment file
echo "🔧 Setting up environment variables..."
cp .env.example .env

# Initialize database
echo "🗄️  Initializing database..."
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python run.py"
echo "3. Open your browser and go to: http://localhost:5000"
echo ""
echo "Happy task managing! 📝"
