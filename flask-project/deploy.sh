#!/bin/bash

# Production Deployment Script for Flask Task Manager

echo "🚀 Deploying Flask Task Manager to Production..."

# Set production environment
export FLASK_ENV=production
export FLASK_APP=run.py

# Install production dependencies
echo "📦 Installing production dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
flask db upgrade

echo "✅ Deployment setup complete!"
echo ""
echo "Environment Variables Required:"
echo "- SECRET_KEY: A secure secret key"
echo "- DATABASE_URL: PostgreSQL connection string"
echo ""
echo "Example DATABASE_URL:"
echo "postgresql://username:password@localhost:5432/taskmanager_db"
