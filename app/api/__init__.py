from flask import render_template, redirect, request, Blueprint, session, url_for
from flask_login import current_user
from app.db import Block, db
import json

# Registers flask blueprint variable for page rendering
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/blocked')
def website():
    if request.method == "POST":
        data = json.loads(request.data)
        block_url = Block(url=data["blocked_url"], block_id=data["block_id"])
        db.session.add(block_url)
        db.session.commit()
