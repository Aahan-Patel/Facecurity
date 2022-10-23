from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, redirect, request, Blueprint, session, url_for, flash
import os
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from app.db import db, Block, db_code
from wtforms import StringField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, Email, Length, AnyOf, EqualTo, ValidationError
import validators
import json
from PIL import Image
from io import BytesIO
import base64
import re
from PIL import Image
from io import BytesIO
import base64
import re
import cv2
import numpy as np
import time
import face_recognition
from os.path import exists

service_blueprint = Blueprint('service', __name__, template_folder='templates')


class Blocked_URL_Form(FlaskForm):
    url = StringField('Blocked URL', validators=[InputRequired(), Length(max=300)])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ["jpeg", "jpg", "png"]

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
        if 'file' in request.files:
            file = request.files['file']
            image_id = current_user.block_id
            file.filename = image_id + "." + (file.filename.split('.'))[-1]
            if file and allowed_file(file.filename):
                image_name = secure_filename(file.filename)
                path = f"app/video/images/{image_name}"
                file.save(path)
    return render_template('verify.html')



@service_blueprint.route('/cam/confirm/<string:block_id>', methods=["POST", "GET"])
@login_required
def confirm(block_id):
    if not exists(f"app/video/images/{current_user.block_id}.png"):
        return redirect(url_for("service.verify"))
    if request.method == "POST":
        image_data = re.sub('^data:image/.+;base64,', '', request.values.get("imgBase64"))
        im = Image.open(BytesIO(base64.b64decode(image_data)))
        image_code = db_code(10)
        im.save("app/video/images/test.png")

        init_img = face_recognition.load_image_file(f"app/video/images/{current_user.block_id}.png")
        first_face = face_recognition.face_encodings(init_img)[0]
        print("first", first_face)

        last_img = face_recognition.load_image_file("app/video/images/test.png")
        last_face = face_recognition.face_encodings(last_img)
        print("last", last_face)
        last_face = last_face[0]

        known_faces = [first_face]
        face_locations = face_recognition.face_locations(last_img)[0]
        name = None
        matches = face_recognition.compare_faces(known_faces, last_face)
        if True in matches:
            print("true detected")
            name = current_user.name

        top, right, bottom, left = 0, 0, 0, 0
        if name != None:
            print('hi')
            location = face_locations
            top, right, bottom, left = location[0] * 4, location[1] * 4, location[2] * 4, location[3] * 4
            index = request.args.get("index")
            url_list = db.session.query(Block).filter(Block.block_id==current_user.block_id).all()
            urls = []
            for i in url_list:
                urls.append(i.url)
            url = urls[int(index)] + "?redirectid=1"
            print("redirect url", url)
            return render_template("confirm.html", urlt = url)
    return render_template('confirm.html', urlt="")
