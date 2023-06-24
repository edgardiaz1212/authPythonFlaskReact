"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from base64 import b64encode
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

def set_password(password, salt):
    return generate_password_hash(f"{password}{salt}")

def check_password(hash_password, password, salt):
    return check_password_hash(hash_password, f"{password}{salt}")


@api.route('/user', methods=['POST'])
def register_user():
    if request.method =="POST":
        data = request.json

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
        
        # Generar una sal aleatoria 
        password_salt = b64encode(os.urandom(32)).decode('utf-8')
       
      # Concatenar la contraseña con la sal
        password_hash = set_password(data.get("password"), password_salt)

        new_user = User(
            name=data.get("name"), 	
            last_name=data.get("last_name"), 	
            email=data.get("email"), 		
            password=password_hash,		
            salt=password_salt		
        )
        
        db.session.add(new_user)
        
        try:
            db.session.commit()
            return jsonify({"msg":"User succefully register"}) ,201
        except Exception as error:
            db.session.rollback()
            return jsonify ({"msg":"Error register user", "error": str(error)}), 500


@api.route('/login', methods=['POST'])
def login():
    if request.method== 'POST':
        data = request.json
        email = data.get("email" ,None)
        password =data.get("password" , None)

        if data is None:
            return jsonify({"msg": "Missing JSON in request"}), 400
        if email is None:
            return jsonify({"msg": "Missing Parameter"}), 400
        if password is None:
            return jsonify({"msg": "Missing Parameter"}), 400

        user = User.query.filter_by(email=email).one_or_none()

        if user is not None:
            if check_password(user.password, password, user.salt):
                # Generar un token de acceso para el usuario
                token = create_access_token(identity=user.id)
                return jsonify({"token": token}), 200
        else:
            return jsonify({"msg": "Bad Credentials"}), 400
        

       
    