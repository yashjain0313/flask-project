#!/bin/bash

# Docker Production Deployment Script

echo "🚀 Deploying Flask Task Manager to Production with Docker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Creating one..."
    echo "Please set the following environment variables in .env:"
    cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://taskmanager:$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)@db:5432/taskmanager_db
FLASK_ENV=production
EOF
    echo "✅ Created .env file with secure random values"
fi

# Load environment variables
source .env

# Build production images
echo "🏗️  Building production Docker images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Start production services
echo "🚀 Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec web flask db upgrade

# Check if services are healthy
echo "🔍 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ Production deployment complete!"
echo ""
echo "🌐 Application is running at: http://localhost"
echo "🔒 For HTTPS, configure SSL certificates in the nginx.conf file"
echo ""
echo "📋 Production management commands:"
echo "  docker-compose -f docker-compose.prod.yml up -d    # Start services"
echo "  docker-compose -f docker-compose.prod.yml down     # Stop services"
echo "  docker-compose -f docker-compose.prod.yml logs web # View app logs"
echo "  docker-compose -f docker-compose.prod.yml restart web # Restart app"
echo ""
echo "🔧 To update the application:"
echo "  git pull"
echo "  docker-compose -f docker-compose.prod.yml build web"
echo "  docker-compose -f docker-compose.prod.yml up -d web"
