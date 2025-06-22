#!/bin/bash

# Docker Development Setup Script

echo "🐳 Setting up Flask Task Manager with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment file for Docker
echo "🔧 Setting up environment variables..."
if [ ! -f .env.docker ]; then
    cat > .env.docker << EOF
FLASK_ENV=development
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://taskmanager:password123@db:5432/taskmanager_db
EOF
    echo "✅ Created .env.docker file"
else
    echo "ℹ️  .env.docker already exists"
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec web flask db upgrade

echo "✅ Setup complete!"
echo ""
echo "🌐 Application is running at: http://localhost:5000"
echo "🗄️  Database admin is available at: http://localhost:8080"
echo "   - Server: db"
echo "   - Username: taskmanager"
echo "   - Password: password123"
echo "   - Database: taskmanager_db"
echo ""
echo "📋 Useful Docker commands:"
echo "  docker-compose up -d          # Start services"
echo "  docker-compose down           # Stop services"
echo "  docker-compose logs web       # View app logs"
echo "  docker-compose exec web bash  # Access app container"
echo "  docker-compose exec db psql -U taskmanager taskmanager_db  # Access database"
