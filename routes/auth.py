from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, redirect, request, Blueprint, session, url_for, flash
import os
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from app.db import db, User, db_code

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


oauth = OAuth()
google = oauth.register(
    name='google',
    client_id="742060573004-j67egluhjhrgnpqpkln7c0t2tur521ar.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'email profile'}
)


@auth_blueprint.route('/auth/login/google', methods=["POST", "GET"])
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_blueprint.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    user = db.session.query(User).filter(User.email == resp["email"]).first()
    if user is None:
        pass
        user = User(type="google", name=resp["name"], email=resp["email"], password=None,
                    profile_picture=resp["picture"], block_id=db_code(7))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('service.dashboard'))


@auth_blueprint.route('/auth/login')
def login():
    return render_template('login.html')


@auth_blueprint.route('/auth/register')
def register():
    return render_template('register.html')
