from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, redirect, request, Blueprint, session, url_for, flash
import os
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from app.db import db, Block, db_code
from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length, AnyOf, EqualTo, ValidationError
import validators
import json
from PIL import Image
from io import BytesIO
import base64
import re

service_blueprint = Blueprint('service', __name__, template_folder='templates')


class Blocked_URL_Form(FlaskForm):
    url = StringField('Blocked URL', validators=[InputRequired(), Length(max=300)])


@service_blueprint.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard():
    blocked_urls = db.session.query(Block).filter(Block.block_id == current_user.block_id).all()
    form = Blocked_URL_Form()
    if form.validate_on_submit():
        if validators.url(form.url.data):
            block_url = Block(url=form.url.data, block_id=current_user.block_id)
            db.session.add(block_url)
            db.session.commit()
            blocked_urls = db.session.query(Block).filter(Block.block_id == current_user.block_id).all()
        else:
            form.url.errors.append("Please enter a valid URL")
        return render_template('dashboard.html', form=form, blocked_urls=blocked_urls)
    return render_template('dashboard.html', form=form, blocked_urls=blocked_urls)


@service_blueprint.route('/cam/verify', methods=["POST", "GET"])
@login_required
def verify():
    if request.method == "POST":
        image_data = re.sub('^data:image/.+;base64,', '', request.values.get("imgBase64"))
        im = Image.open(BytesIO(base64.b64decode(image_data)))
        image_code = db_code(10)
        image_path = r".\\app\\video\\images\\" + current_user.block_id + ".png"
        im.save(image_path)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return render_template('verify.html')

