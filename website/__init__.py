from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blockchain.db'
    app.config['SECRET_KEY'] = '1234567890'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .models import User, Wallet, Transaction
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    #login_manager.login_view =
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + 'blockchain.db'):
        db.create_all(app=app)
        print('Created Database')
