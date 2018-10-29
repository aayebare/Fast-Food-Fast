import datetime
from flask import Flask, request, jsonify
from app import app
from app.models.user_models import User
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flasgger import swag_from

now = datetime.datetime.now()


@app.route('/api/v1/auth/signup', methods=['POST'])
@cross_origin()
@swag_from('../docs/signup.yml')
def register():
    '''registering a new user'''
    input_data = request.get_json()
  
    if 'password' not in input_data or input_data['password'].strip() == "":
        return jsonify({"message": "please add password"}), 400
   
    elif input_data.get('user_name') == None and input_data.get('email') == None:
        return jsonify({
            "message":
            "please add a username and/or email and try again"
        }), 400
    elif 'username' not in input_data or input_data['username'].strip() == "":
        return jsonify({
            "message": "please, add a username and try again"
        }), 400
    elif input_data.get('email').strip() == "":
        return jsonify({"message": "please add an email and try again"}), 400

    elif 'confirm_password' not in input_data or input_data.get('confirm_password').strip() == "":
            return jsonify({"message": "please confirm-password"}), 400
            
    elif input_data['password'] != input_data['confirm_password']:
        return jsonify({
            "message": "passwords do not match, please try again!!"
        }), 400    

    elif not re.match("[^@]+@[^@]+\.[^@]+", input_data['email']):
        return jsonify({
            "message": "please fill in a valid email address"
        }), 400
    elif 'is_admin' not in input_data or type(
            input_data['is_admin']) is not bool:
        return jsonify({"message": "please add a valid account type"}), 400

    user = User(input_data['username'].lower(), input_data['email'].lower(),
                generate_password_hash(input_data['password']),
                input_data['is_admin'])
    '''check if email exits in the database'''
    user_email = User(None, input_data['email'].lower(), None, None)
    find_duplicate = user_email.check_duplicate()

    if find_duplicate:
        return jsonify({
            "message":
            "this email already exists, please use a different email to signup"
        }), 400
    '''add user to the database'''
    user.add_user()

    return jsonify({"message": "registration was successful"}), 201


@app.route('/api/v1/auth/login', methods=['POST'])
@cross_origin()
@swag_from('../docs/login.yml')
def login():
    '''logging in a user'''
    input_data = request.get_json()
    if 'email' not in input_data or input_data['email'].strip() == "":
        return jsonify({"message": "please add an email in order to login"}), 400
    if type(input_data['password']) is not str:
        return jsonify({
            "message":
            "please add a valid password in order to login"
        }), 400

    if 'password' not in input_data or input_data['password'].strip() == "":
        return jsonify({"message": "please add a password in order to login"}), 400

    user = User(None, input_data['email'].lower(), None, None)
    '''check for existing email in the database'''
    find_duplicate = user.check_duplicate()
    if find_duplicate:
        result = user.login_user()
        
        hashed_password = check_password_hash(result[1],
                                              input_data['password'])
        '''check user password'''
        if hashed_password:
            token = create_access_token(identity=result[0])
            
            is_admin = user.check_admin()
            print(is_admin)
            if is_admin[0]==True:
                return jsonify({
                    "token": token,
                    "message": "User successfully logged in as admin"
                }), 200
            else:
                return jsonify({
                    "token": token,
                    "message": "User successfully logged in"
                }), 200

        else:
            return jsonify({
                "message": "Incorrect password, please try again"
            }), 400
    else:
        return jsonify({
            "message":
            "Incorrect email,please try again or signup!!"
        }), 404
