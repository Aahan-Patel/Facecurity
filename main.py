from flask import Flask, render_template, redirect, request, Blueprint, url_for
import os
from flask_bootstrap import Bootstrap5
from routes.auth import auth_blueprint
from routes.services import service_blueprint
from routes.info import info_blueprint
from routes.auth import auth_blueprint, login_manager, oauth
from app.api import api_blueprint
from app.db import db

template_dir = os.path.abspath('views/templates')
static_dir = os.path.abspath('views/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
boostrap = Bootstrap5()

# Registering blueprints
app.register_blueprint(info_blueprint, url_prefix="")
app.register_blueprint(service_blueprint, url_prefix="")
app.register_blueprint(auth_blueprint, url_prefix="")
app.register_blueprint(api_blueprint, url_prefix="")


with app.app_context():
    app.config['SECRET_KEY'] = "ADSJ234234AJIHJ"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == "__main__":
    login_manager.init_app(app)
    boostrap.init_app(app)
    db.init_app(app)
    with app.app_context(): 
        db.create_all()
    oauth.init_app(app)
    app.run()
