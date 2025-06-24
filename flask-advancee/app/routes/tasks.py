from flask import render_template,Blueprint,flash,url_for,redirect,request,flash,session
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks',__name__)

@tasks_bp.route("/")
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()
    return render_template('task.html',tasks=tasks)


@tasks_bp.route("/add", methods=["POST"])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title=request.form.get('title')
    if title:
         new_task = Task(title=title, status='Pending')
         db.session.add(new_task)
         db.session.commit()
         flash('Task added successfully','success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>',methods=['POST'])
def toggle_status(task_id):
    task= Task.query.get(task_id)
    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
             task.status = "Done"   
        else:
            task.status = "Pending" 

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))  



@tasks_bp.route("/clear",methods=["POST"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash("All tasks cleared","info")
    return redirect(url_for("tasks.view_tasks"))


            


    
   


