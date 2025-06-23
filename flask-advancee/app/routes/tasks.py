from flask import render_template,Blueprints,flash,url_for,redirect,request,flash,session
from app import db
from app.models import Task

tasks_bp = Blueprints('tasks',__name__)

@tasks_bp.route("/")
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Tasks.query.all()
    return render_template('tasks.html',tasks=tasks)


@tasks_bp.route("/add")
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    new_task = Task(title=title , status='pending')
    db.session.add('new_task')


