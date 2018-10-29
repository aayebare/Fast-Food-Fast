import datetime
from flask import Flask, request, jsonify
from app import app
from app.models.menu_models import Menu
from app.models.user_models import User
from flasgger import swag_from  
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
                                
                              

now = datetime.datetime.now()


@app.route('/api/v1/menu', methods=['POST', 'GET'])
@cross_origin()
@jwt_required
@swag_from('../docs/post_and_get_menu_items.yml')
def menu():
    if request.method == 'GET':
        '''get all food items in the menu'''
        data = Menu(None, None, None, None, None)
        result = data.get_menu()
        return jsonify(result), 200
    else:
        '''add food items in the menu'''
        current_user = get_jwt_identity()
        is_admin = User.check_user_role(current_user)
        
        if is_admin[0] == True:
            input_data = request.get_json()
            current_user = get_jwt_identity()
            if input_data.get('content') == None or input_data.get(
                    'detail') == None or input_data.get('price') == None:
                return jsonify({"message": "Please add content or detail or price fields"}), 400
                
            if input_data.get('content').strip()=="":
                return jsonify({'message':"Please add value in the content field"}), 400  

            # if type(input_data['price']) is not float:
            #     return jsonify({"message": "Please add valid unit price"}), 400
            if input_data.get('price') == "":
                 return jsonify({"message": "Please add a unit price"}), 400

            new_item = Menu(current_user, None, input_data['content'],
                            input_data['detail'], input_data['price'])

            new_item.add_item()
            return jsonify({"success": "Item successfully posted"}), 200
        else:
            return jsonify({
                "message":
                "Admin previledges required to perform this function"
            }), 401
