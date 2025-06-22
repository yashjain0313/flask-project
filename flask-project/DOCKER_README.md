# 🐳 Docker Setup and Deployment Guide

## Complete Docker Setup for Flask Task Manager

Your Flask application is now fully Docker-ready! Here's everything you need to know.

## 📋 Prerequisites

1. **Install Docker Desktop:**

   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Verify installation: `docker --version`

2. **Start Docker Desktop** (if not running automatically)

## 🚀 Quick Start Commands

### Development Environment

```bash
# 1. Start Docker Desktop first!

# 2. Build and run with one command
./docker-setup.sh

# Or manually:
docker-compose up -d

# 3. Access your application
# App: http://localhost:5000
# Database Admin: http://localhost:8080
```

### Production Environment

```bash
# 1. Deploy to production
./docker-deploy.sh

# Or manually:
docker-compose -f docker-compose.prod.yml up -d

# 2. Access your application
# App: http://localhost (port 80)
```

## 📁 Docker Files Created

✅ **Dockerfile** - Main container configuration
✅ **docker-compose.yml** - Development environment
✅ **docker-compose.prod.yml** - Production environment  
✅ **nginx.conf** - Reverse proxy configuration
✅ **entrypoint.sh** - Container startup script
✅ **.dockerignore** - Files to exclude from build
✅ **docker-setup.sh** - Development setup script
✅ **docker-deploy.sh** - Production deployment script

## 🔧 What Docker Gives You

### Development Benefits:

- **Consistent Environment** - Same setup on any machine
- **Easy Database** - PostgreSQL ready with one command
- **Hot Reload** - Code changes reflect immediately
- **Database Admin** - Adminer at localhost:8080

### Production Benefits:

- **Scalability** - Easy to scale with multiple containers
- **Security** - Isolated environment with non-root user
- **Load Balancing** - Nginx reverse proxy included
- **Health Checks** - Automatic service monitoring
- **Zero Downtime** - Rolling updates support

## 📊 Architecture

```
Development:
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Browser   │───▶│  Flask App   │───▶│ PostgreSQL  │
│ :5000       │    │  (Python)    │    │  Database   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                   ┌──────────────┐
                   │   Adminer    │
                   │   :8080      │
                   └──────────────┘

Production:
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│   Browser   │───▶│    Nginx     │───▶│  Flask App   │───▶│ PostgreSQL  │
│   :80       │    │ (Load Bal.)  │    │  (Gunicorn)  │    │  Database   │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
```

## 🛠️ Essential Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Restart specific service
docker-compose restart web

# Check running containers
docker-compose ps
```

### Database Operations

```bash
# Run migrations
docker-compose exec web flask db upgrade

# Access database
docker-compose exec db psql -U taskmanager taskmanager_db

# Backup database
docker-compose exec db pg_dump -U taskmanager taskmanager_db > backup.sql
```

### Development Workflow

```bash
# Make code changes...
# Services automatically reload!

# Add new dependencies to requirements.txt
docker-compose build web
docker-compose up -d web

# Run tests (when added)
docker-compose exec web python -m pytest
```

## 🌐 Deployment Options

### Option 1: Local Production Test

```bash
./docker-deploy.sh
# Access at http://localhost
```

### Option 2: Cloud Deployment (DigitalOcean, AWS, etc.)

```bash
# 1. Copy files to server
scp -r . user@your-server:/app

# 2. SSH into server
ssh user@your-server

# 3. Deploy
cd /app
./docker-deploy.sh
```

### Option 3: Container Services

- **AWS ECS**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**

## 🔒 Security Features

✅ **Non-root user** in container
✅ **Security headers** in Nginx
✅ **Environment variable** isolation
✅ **Network isolation** between services
✅ **Health checks** for monitoring
✅ **Minimal attack surface** with Alpine Linux

## 📈 Scaling Options

### Horizontal Scaling

```bash
# Scale Flask app to 3 instances
docker-compose up -d --scale web=3

# Nginx automatically load balances
```

### Vertical Scaling

```yaml
# In docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"
```

## 🔧 Customization

### Environment Variables

Edit `.env` file:

```bash
SECRET_KEY=your-super-secret-key
DATABASE_URL=postgresql://user:pass@db:5432/dbname
FLASK_ENV=production
```

### Nginx Configuration

Edit `nginx.conf` for:

- SSL/HTTPS setup
- Custom domain
- Load balancing rules
- Static file serving

### Database Configuration

Edit `docker-compose.yml`:

```yaml
db:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: your_db_name
    POSTGRES_USER: your_username
    POSTGRES_PASSWORD: your_password
```

## 🚨 Troubleshooting

### Common Issues

1. **Docker not running:**

   ```bash
   # Start Docker Desktop application
   # Check: docker --version
   ```

2. **Port conflicts:**

   ```bash
   # Change ports in docker-compose.yml
   ports:
     - "5001:5000"  # Use 5001 instead of 5000
   ```

3. **Database connection issues:**

   ```bash
   # Check database logs
   docker-compose logs db

   # Restart database
   docker-compose restart db
   ```

4. **Permission errors:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

## 💡 Pro Tips

1. **Use .env files** for different environments
2. **Regular backups** with automated scripts
3. **Monitor logs** with `docker-compose logs -f`
4. **Update regularly** with `docker-compose pull`
5. **Clean up** with `docker system prune`

## 🎯 Next Steps

1. **Start Docker Desktop**
2. **Run `./docker-setup.sh`**
3. **Visit http://localhost:5000**
4. **Create your first task!**

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Flask Production Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [PostgreSQL Docker Guide](https://hub.docker.com/_/postgres)

---

Your Flask Task Manager is now production-ready with Docker! 🎉
