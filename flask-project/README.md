# Flask Task Manager

A modern task management web application built with Flask, featuring user authentication, task CRUD operations, and a responsive UI.

## Features

- User Registration and Authentication
- Create, Read, Update, Delete Tasks
- Task Categories and Priority Levels
- Responsive Design with Bootstrap
- SQLite Database with SQLAlchemy ORM
- Form Validation with WTForms
- Flash Messages for User Feedback

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. Run the application:
   ```bash
   python run.py
   ```

## Usage

1. Register a new account or login with existing credentials
2. Create tasks with title, description, category, and priority
3. Mark tasks as completed
4. Edit or delete existing tasks
5. Filter tasks by category or completion status

## Project Structure

```
flask-project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── migrations/
├── requirements.txt
├── config.py
├── run.py
└── .env
```

## Technologies Used

- Python 3.8+
- Flask 3.0
- SQLAlchemy
- Bootstrap 5
- SQLite
