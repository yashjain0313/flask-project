# PostgreSQL Setup Instructions

## Local PostgreSQL Installation (macOS)

### 1. Install PostgreSQL

```bash
brew install postgresql@15
brew services start postgresql@15
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE taskmanager_db;
CREATE USER taskmanager WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE taskmanager_db TO taskmanager;
\q
```

### 3. Update .env file

```bash
DATABASE_URL=postgresql://taskmanager:your_password@localhost:5432/taskmanager_db
```

### 4. Install PostgreSQL driver

```bash
pip install psycopg2-binary
```

### 5. Run migrations

```bash
flask db upgrade
```

## Production Database Services

### 1. ElephantSQL (Free tier available)

- Sign up at elephantsql.com
- Create new instance
- Copy connection URL to DATABASE_URL

### 2. Supabase (PostgreSQL with extras)

- Sign up at supabase.com
- Create new project
- Get connection string from settings

### 3. PlanetScale (MySQL alternative)

- Sign up at planetscale.com
- Create database
- Get connection string

### 4. Neon (Serverless PostgreSQL)

- Sign up at neon.tech
- Create database
- Copy connection string

## Database URL Formats

### PostgreSQL

```
postgresql://username:password@hostname:port/database_name
```

### MySQL (if using PlanetScale)

```
mysql://username:password@hostname:port/database_name
```

### SQLite (development only)

```
sqlite:///path/to/database.db
```

## Environment Variables for Production

Set these environment variables in your deployment platform:

```bash
SECRET_KEY=your-super-secret-key-min-32-characters
DATABASE_URL=your-database-connection-string
FLASK_ENV=production
```

## Migration Commands

```bash
# Initialize migrations (first time only)
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Downgrade (if needed)
flask db downgrade
```
