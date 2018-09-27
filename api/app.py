from flask import Flask, jsonify, request
import json
import datetime

app = Flask(__name__)
now = datetime.datetime.now()

all_orders = [
    {
			"id":1,
			"content":"shuwarma",
			"price":100,
			'date': '12-9-18',
			"completed":False
	}

            ]

@app.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    '''Getting all orders'''
    if request.method == 'GET':
        return jsonify(all_orders), 200   
    else:
        '''Post an order''' 
        post_order = request.get_json()
        ''''Check against empty content field in order'''
        if 'content' not in post_order or post_order['content'].strip()=="": 
            return jsonify({"message":"No order made,please add order and try again"}), 400 
        '''check for price in order'''    
        if 'price' in post_order:
            if type(post_order['price']) is int or type(post_order['price']) is float:
                '''create new order and add it to all_orders'''
                new_order = {
                    "id":len(all_orders)+1,
                    "content":post_order["content"],
                    "price":post_order["price"],
                    "date":now.strftime("%Y-%m-%d"),
                    "completed":False
                }
                all_orders.append(new_order)
                return jsonify(new_order), 201
            else:    
                return jsonify ({"message":"please add a valid unit price"}), 400  
        else:
            return jsonify({"message":"This order has no price, please verify the price and try again"}), 400

@app.route('/api/v1/orders/<int:order_id>', methods=['GET', 'PUT'])
def single_order(order_id):
    '''Getting a single order''' 
    get_order = [order for order in all_orders if order['id'] == order_id]
    if len(get_order) == 0:
            return jsonify({"message":"no order with the given id, please try again"}), 404 #not found
    if request.method == 'GET':        
        return jsonify(get_order[0]), 200
    else:
        '''Updating the status of an order'''
        input_order = request.get_json()
        if 'completed' in input_order:
            '''Check for boolean type status'''
            if type(input_order["completed"]) is bool:
                ''''update status of order'''
                get_order[0]["completed"] = input_order["completed"]
                return jsonify(get_order[0]), 200
            else:  
                return jsonify({"message":"please add a boolean value to change the status"}), 400
        else:
            return jsonify({"message":"please add a new status"}), 400