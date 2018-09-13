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

