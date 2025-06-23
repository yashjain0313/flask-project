from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app():
    app=Flask(__name__)

    app.config['SECRET KEY']="yashjain"
    app.config['SQLALCHEMY_DB_URI']="sqlite:///todo.db"
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False

    db.__init__(app)
    from app.routes.auth import auth_bp
    from app.routes.auth import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return


