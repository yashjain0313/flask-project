# Docker Deployment Guide

This guide covers how to deploy the Flask Task Manager using Docker.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)

## Quick Start

### Development Environment

1. **Clone and setup:**

```bash
cd flask-project
./docker-setup.sh
```

2. **Access the application:**

- App: http://localhost:5000
- Database Admin: http://localhost:8080

### Production Environment

1. **Deploy to production:**

```bash
./docker-deploy.sh
```

2. **Access the application:**

- App: http://localhost (port 80)

## Docker Compose Files

### `docker-compose.yml` (Development)

- Flask app with hot reload
- PostgreSQL database
- Adminer for database management
- Debug mode enabled

### `docker-compose.prod.yml` (Production)

- Optimized Flask app
- PostgreSQL database
- Nginx reverse proxy
- Health checks
- Production-ready configuration

## Manual Docker Commands

### Build and Run

```bash
# Build the Docker image
docker build -t flask-taskmanager .

# Run with PostgreSQL
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Database Operations

```bash
# Run migrations
docker-compose exec web flask db upgrade

# Access database shell
docker-compose exec db psql -U taskmanager taskmanager_db

# Backup database
docker-compose exec db pg_dump -U taskmanager taskmanager_db > backup.sql

# Restore database
docker-compose exec -T db psql -U taskmanager taskmanager_db < backup.sql
```

### Application Management

```bash
# Access application shell
docker-compose exec web bash

# View application logs
docker-compose logs web

# Restart application
docker-compose restart web

# Update application
git pull
docker-compose build web
docker-compose up -d web
```

## Environment Variables

Create a `.env` file for production:

```bash
SECRET_KEY=your-super-secret-key-minimum-32-characters
DATABASE_URL=postgresql://taskmanager:secure_password@db:5432/taskmanager_db
FLASK_ENV=production
```

## Production Deployment Options

### Option 1: Single Server

```bash
# Deploy to single server
scp -r . user@server:/app
ssh user@server "cd /app && ./docker-deploy.sh"
```

### Option 2: Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml taskmanager
```

### Option 3: Kubernetes

See `k8s/` directory for Kubernetes manifests.

## SSL/HTTPS Setup

1. **Obtain SSL certificates** (Let's Encrypt recommended):

```bash
mkdir ssl
# Copy your cert.pem and key.pem to ssl/ directory
```

2. **Update nginx.conf** to enable HTTPS section

3. **Restart services:**

```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

## Monitoring and Logging

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Follow logs
docker-compose logs -f web
```

### Container Status

```bash
# Check running containers
docker-compose ps

# Check resource usage
docker stats
```

### Health Checks

```bash
# Check application health
curl http://localhost:5000/

# Check database health
docker-compose exec db pg_isready -U taskmanager
```

## Backup and Restore

### Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U taskmanager taskmanager_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U taskmanager taskmanager_db > "backups/backup_$DATE.sql"
gzip "backups/backup_$DATE.sql"
```

### Application Data Backup

```bash
# Backup uploaded files (if any)
docker cp $(docker-compose ps -q web):/app/uploads ./backups/uploads_$(date +%Y%m%d_%H%M%S)
```

### Restore from Backup

```bash
# Restore database
docker-compose exec -T db psql -U taskmanager taskmanager_db < backup.sql

# Restore uploaded files
docker cp ./uploads $(docker-compose ps -q web):/app/
```

## Scaling

### Horizontal Scaling

```bash
# Scale web service
docker-compose up -d --scale web=3

# Use with load balancer
# Update nginx.conf upstream section
```

### Vertical Scaling

Update docker-compose.yml:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"
```

## Troubleshooting

### Common Issues

1. **Port already in use:**

```bash
# Find process using port
sudo lsof -i :5000
# Kill process or change port in docker-compose.yml
```

2. **Database connection issues:**

```bash
# Check database logs
docker-compose logs db
# Restart database
docker-compose restart db
```

3. **Permission issues:**

```bash
# Fix ownership
sudo chown -R $USER:$USER .
```

4. **Out of disk space:**

```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Debug Mode

Enable debug mode in development:

```bash
# Set environment variable
export FLASK_DEBUG=1
docker-compose up
```

## Security Considerations

1. **Change default passwords**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS in production**
4. **Regular security updates:**

```bash
# Update base images
docker-compose pull
docker-compose up -d
```

5. **Firewall configuration:**

```bash
# Only expose necessary ports
# Use Docker networks for internal communication
```

## Performance Optimization

### Docker Image Optimization

- Multi-stage builds
- Minimal base images
- Layer caching

### Database Optimization

- Connection pooling
- Database indexes
- Query optimization

### Nginx Optimization

- Gzip compression
- Static file caching
- Connection limits

## Maintenance

### Regular Tasks

```bash
# Weekly maintenance script
#!/bin/bash
# Backup database
./backup.sh

# Update images
docker-compose pull

# Clean up old images
docker image prune -f

# Restart services
docker-compose up -d
```

### Monitoring Script

```bash
#!/bin/bash
# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "Service down, restarting..."
    docker-compose up -d
fi
```
