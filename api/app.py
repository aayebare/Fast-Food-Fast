from flask import Flask, jsonify, request
import json
import datetime


app = Flask(__name__)

now = datetime.datetime.now()

all_orders = [
    {
        "id":1,
        "content":"Shuwarma",
        "price":100,
        "date":"12-9-18",
        "completed":False
        }
    ]

@app.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    #Getting all orders
    if request.method == 'GET':
        return jsonify(all_orders), 200
    #Post an order    
    else:
        post_order = request.get_json()
        #Check for empty content field in order
        if 'content' not in post_order or post_order['content'].strip()=="": 
            return jsonify("No order made,please add order and try again"), 400 
        #Check for empty price field in order
        if 'price' not in post_order or post_order['price']==" ":
            return jsonify("This order has no price, please verify the price and try again"), 400 
        if type(post_order['price']) is not int:
             return jsonify ("please add a valid unit price"), 400   
        #create new order and add it to all_orders
        new_order = {
            "id":len(all_orders)+1,
            "content":post_order["content"],
            "price":post_order["price"],
            "date":now.strftime("%Y-%m-%d"),
            "completed":False
        }
        all_orders.append(new_order)
        return jsonify(new_order), 201

@app.route('/api/v1/orders/<int:order_id>', methods=['GET', 'PUT'])
def single_order(order_id):
    #Getting a single order 
    get_order = [order for order in all_orders if order['id'] == order_id]
    if len(get_order) == 0:
            return jsonify("no order with the given id, please try again"), 404 #not found
    if request.method == 'GET':        
        return jsonify(get_order[0]), 200
    #Updating the status of an order
    else:
        input_order = request.get_json()
        if 'completed' not in input_order:
            return jsonify("please add a new status"), 400
        #Check if status is of type boolean
        if type(input_order["completed"]) is not bool:
            return jsonify("please add a boolean value to change the status"), 400
        #Check if order already completed    
        if get_order[0]['completed'] and input_order['completed']==True:
            return jsonify("order already completed"), 200
        #update status of order
        get_order[0]["completed"] = input_order["completed"]
        return jsonify(get_order[0]), 200