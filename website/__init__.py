from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate


# "postgresql://user_name:password@IP:5432/db_name"
db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Flask website123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_name:password@IP:5432/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


def create_app():
    # URL
    from .views import views
    from .auth import auth
    from .work_log import wlog

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(wlog, url_prefix='/wlog')

    # DB
    from .models import User, WorkLog
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')
