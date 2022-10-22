from flask import render_template, redirect, request, Blueprint, session, url_for
from flask_login import current_user
from app.db import User

# Registers flask blueprint variable for page rendering
info_blueprint = Blueprint('information', __name__)

# Renders info page html
@info_blueprint.route('/home')
def home():
    return render_template('home.html')


# Redirects users from standard url to info page url
@info_blueprint.route('/')
def website():
    return redirect(url_for('information.home'))

@info_blueprint.route('/tos')
def tos(): 
    return render_template('tos.html')