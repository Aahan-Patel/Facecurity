from flask import render_template, redirect, request, Blueprint, session, url_for
from flask_login import current_user
from app.db import Block, db, User
import json

# Registers flask blueprint variable for page rendering
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/blocked')
def block():
    if request.method == "POST":
        data = json.loads(request.data)
        block_url = Block(url=data["blocked_url"], block_id=data["block_id"])
        db.session.add(block_url)
        db.session.commit()

@api_blueprint.route('/login')
def login():
    if request.method == "POST":
        data = json.loads(request.data)
        user = db.session.query(User).filter(User.email == data["email"]).filter(User)
        db.session.add(block_url)
        db.session.commit()
