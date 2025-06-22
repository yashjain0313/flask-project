from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import TaskForm
from app.models import Task

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html', title='Task Manager')
    
    # Get filter parameters
    category = request.args.get('category')
    status = request.args.get('status')
    
    # Base query for current user's tasks
    query = Task.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    if status == 'completed':
        query = query.filter_by(completed=True)
    elif status == 'pending':
        query = query.filter_by(completed=False)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
    # Get all categories for filter dropdown
    categories = db.session.query(Task.category).filter_by(user_id=current_user.id).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('dashboard.html', title='Dashboard', tasks=tasks, categories=categories)

@bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            completed=form.completed.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('task_form.html', title='New Task', form=form, legend='New Task')

@bp.route('/task/<int:id>')
@login_required
def task_detail(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('task_detail.html', title=task.title, task=task)

@bp.route('/task/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = TaskForm()
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.category = form.category.data
        task.priority = form.priority.data
        task.completed = form.completed.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('main.task_detail', id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.category.data = task.category
        form.priority.data = task.priority
        form.completed.data = task.completed
    
    return render_template('task_form.html', title='Edit Task', form=form, legend='Edit Task')

@bp.route('/task/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/task/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    status = 'completed' if task.completed else 'marked as pending'
    flash(f'Task "{task.title}" {status}!', 'success')
    return redirect(url_for('main.index'))
