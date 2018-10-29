import datetime
from flask import Flask, request, jsonify
from app import app
from app.models.order_models import Orders
from app.models.user_models import User
from app.models.menu_models import Menu
from flasgger import swag_from
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

now = datetime.datetime.now()


@app.route('/api/v1/users/orders', methods=['GET', 'POST'])
@jwt_required
@swag_from('../docs/post_order.yml')
def order():
    '''posting an order'''
    current_user = get_jwt_identity()
    date_post = now.strftime('%d-%m-%y')
    
    if request.method == 'POST':
        input_data = request.get_json()
        if 'item_id' not in input_data:
            return jsonify({"message": "Please add an order"}), 400
        if type(input_data['item_id']) is not int:
            return jsonify({
                "message": "Please, add valid input and try again"
            }), 400

  

        menu_item = Menu(None, input_data['item_id'], None, None, None)
        item = menu_item.get_item_id()
        
        #print(item)

        if item == False:
            return jsonify({
                "message":
                "Item is not available on the menu, please make another order"
            }), 404  
        #print(menu_item.get_Item_Detail())
        new_order = Orders(current_user, input_data['item_id'], None,
                           date_post,menu_item.get_Item_Detail()[0])

        



        new_order.post_order()
        return jsonify({"message": "Order successfully placed"}), 200
    else:
        data = Orders(current_user, None, None, None, None, None)
        result = data.get_user_orders()
        return jsonify(result), 200



@app.route('/api/v1/orders', methods=['GET'])
@jwt_required
@swag_from('../docs/get_all_orders.yml')
def admin_order():
    '''get all orders in the database'''
    current_user = get_jwt_identity()

    is_admin = User.check_user_role(current_user)
    if is_admin[0] == True:
        '''check if user is admin'''
        new_data = Orders(None, None, None, None, None, None)
        result = new_data.get_admin_orders()
        return jsonify(result), 200
    else:
        return jsonify({
            "message":
            "Admin previledges required to perform this function"
        }), 401


@app.route('/api/v1/​​orders​/<int:order_id>', methods=['GET'])
@jwt_required
@swag_from('../docs/get_single_order.yml')
def single_order(order_id):
    '''get a single order'''
    current_user = get_jwt_identity()
    is_admin = User.check_user_role(current_user)

    if is_admin[0] == True:
        '''check if user is admin'''
        data = Orders(None, None, order_id, None, None, None)
        result = data.get_single_order()
        if result == []:
            return jsonify({
            "message":
            "The requested order doesn't exist"
        }), 404
        return jsonify(result), 200
    else:
        return jsonify({
            "message":
            "Admin previledges required to perform this function"
        }), 401


@app.route('/api/v1/​​orders​/<int:order_id>', methods=['PUT'])
@jwt_required
@swag_from('../docs/update_order_status.yml')
def update_status(order_id):
    '''update the satatus of an order'''
    current_user = get_jwt_identity()
    is_admin = User.check_user_role(current_user)

    if is_admin[0] == True:
        '''check if user is admin'''
        input_data = request.get_json()
        if 'order_status' not in input_data:
            return jsonify({"message": "please add a status response"}), 400

        if input_data['order_status'] == "new" or input_data[
                'order_status'] == "processing" or input_data[
                    'order_status'] == "cancelled" or input_data[
                        'order_status'] == "complete":
            data = Orders(None, None, order_id, None, None,
                          input_data['order_status'])
            data.update_order()
            return jsonify({"message": "order succesfully updated"}), 200
        else:
            return jsonify({"message": "please add valid status response"}), 400
    else:
        return jsonify({
            "message":
            "Admin previledges required to perform this function"
        }), 401
