import ska as ska
from flask import render_template, redirect, request, Blueprint, session, url_for, make_response
from flask_login import current_user
from app.db import Block, db, User
import json

SECRET_KEY = "JSD87FS890sd889dfik99FDFD"

# Registers flask blueprint variable for page rendering
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/blocked', methods=["GET", "POST"])
def block():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        block_url = Block(url=data["blocked_url"], block_id=data["block_id"])
        db.session.add(block_url)
        db.session.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@api_blueprint.route('/extension/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            blocked_urls = []
            for i in db.session.query(Block).filter(Block.block_id==current_user.block_id).all():
                blocked_urls.append(i.url)
            print({"registered": True, "email": current_user.email, "block_id": current_user.block_id, "blocked_urls": blocked_urls})
            return {"registered": True, "email": current_user.email, "block_id": current_user.block_id, "blocked_urls": blocked_urls}
        else:
            url = 'https://127.0.0.1:5000/login'
            signed_url = ska.sign_url(
                auth_user='user',
                secret_key=SECRET_KEY,
                url=url
            )
            return {"registered": False, "signed_url": signed_url}
