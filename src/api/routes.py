"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from base64 import b64encode 
import os

api = Blueprint('api', __name__)

def set_password(password, salt):
    return generate_password_hash(f"{password}{salt}")

def check_password(hash_password, pasword, salt):
    return check_password_hash(hash_password,f"{password}{salt}")


@api.route('/user', methods=['POST'])
def all_user():
    data=request.json

    if data is None:
        return jsonify({"msg":"Missing JSON in request"}), 400
    if data.get("name") is None:
        return jsonify({"msg":"Missing Parameter"}), 400
    if data.get("last_name") is None:
        return jsonify({"msg":"Missing Parameter"}), 400
    if data.get("email") is None:
        return jsonify({"msg":"Missing Parameter"}), 400
    if data.get("password") is None:
        return jsonify({"msg":"Missing Parameter"}), 400
    
    user=User.query.filter_by(email=data.get("email")).first()
    if user is not None:
        return jsonify({"msg":"Email already in use"}), 400
    
    password_salt = b64encode(os.urandom(32)).decode('utf-8')
    password_hash = set_password(data.get("password"), password_salt)

    new_user = User(
        name=data.get("name"), 	# name of the user
        last_name=data.get("last_name"), 	# last name of the user
        email=data.get("email"), 		# e-mail of the user
        password=password_hash,		# password of the user, encrypted with salt
        password_salt=password_salt		# password salt, encrypted with password_salt
    )
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"msg":"User succefully register"}) ,201
    except Exception as error:
        db.session.rollback()
        return jsonify ({"msg":"Error register user", "error": str(error)}), 500
  

  