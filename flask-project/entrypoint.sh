#!/bin/bash

# Docker entrypoint script

set -e

echo "🐳 Starting Flask Task Manager..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
while ! pg_isready -h "${DATABASE_URL#*@}" -p 5432 -U taskmanager; do
    echo "Database is unavailable - sleeping"
    sleep 1
done

echo "✅ Database is ready!"

# Run database migrations
echo "🗄️  Running database migrations..."
flask db upgrade

# Create initial admin user if it doesn't exist
python << EOF
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@taskmanager.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Created admin user (username: admin, password: admin123)")
    else:
        print("ℹ️  Admin user already exists")
EOF

echo "🚀 Starting application..."
exec "$@"
