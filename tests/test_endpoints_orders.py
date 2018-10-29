
import unittest
import json 
from app import app
from app.models import Database

db = Database()
class TestingEndpoints(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self) 
        db.create_tables()
        self.response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"adria@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
            )
        self.response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"adria@gmail.com", "password":"ayeb"}),
            content_type='application/json', 
        )
        #raise Exception(self.response)
        self.token=json.loads(self.response.data.decode())["token"]

    def test_user_history_of_orders_returned(self):

        response = self.tester.get(
           '/api/v1/users/orders',
            headers= dict(Authorization='Bearer '+ self.token),
            content_type='application/json' 
        )
        self.assertEqual(response.status_code,200)

    def test_for_succesful_post_order(self):
        self.tester.post(
           '/api/v1/menu',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"content":"food","detail":"mmmmeme","price":24555.9}),
            content_type='application/json'
             )
        
        response= self.tester.post(
           '/api/v1/users/orders',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"item_id":1}),
            content_type='application/json'
             )
        self.assertEqual(response.status_code,200) 
        self.assertIn(b'Order successfully placed',response.data)

    def test_for_empty_post_order(self):

        response = self.tester.post(
           '/api/v1/users/orders',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({}),
            content_type='application/json'
             )
        self.assertEqual(response.status_code,400) 
        self.assertIn(b"Please add an order", response.data)

    def test_for_non_int_item_id_on_post_order(self):
        response = self.tester.post(
           '/api/v1/users/orders',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"item_id":"yu"}),
            content_type='application/json'
             )
        self.assertEqual(response.status_code,400) 
        self.assertIn(b"Please, add valid input and try again", response.data)  

    def test_for_unavailable_item_id(self):
        self.tester.post(
           '/api/v1/menu',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"content":"food","detail":"mmmmeme","price":24555.9}),
            content_type='application/json'
             )
        response = self.tester.post(
           '/api/v1/users/orders',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"item_id":200}),
            content_type='application/json'
             )
        self.assertEqual(response.status_code,404) 
        self.assertIn(b"Item is not available on the menu, please make another order", response.data)

    def test_for_unsuccesfull_return_of_orders_by_non_admin(self):  
        self.tester.post(
        '/api/v1/auth/signup',
        data=json.dumps({
            "username":"ayebare" ,
            "email":"ad@gmail.com",
            "password":"ayeb", 
            "confirm_password":"ayeb",
            "is_admin":False}),
        content_type='application/json'
        )

        response_1 = self.tester.post(
        '/api/v1/auth/login',
        data=json.dumps({"email":"ad@gmail.com", "password":"ayeb"}),
        content_type='application/json', 
        )

        token=json.loads(response_1.data.decode())["token"]  
        response = self.tester.get(
        '/api/v1/orders',
        headers= dict(Authorization='Bearer '+ token),
        content_type='application/json'
            )
        self.assertEqual(response.status_code, 401)  
        self.assertIn(b"Admin previledges required to perform this function", response.data)  

    def test_for_succesfull_return_of_orders_by_admin(self):
        response = self.tester.get(
            '/api/v1/orders',
            headers= dict(Authorization='Bearer '+ self.token),
            content_type='application/json'
                )
        self.assertEqual(response.status_code, 200)  

    def test_for_successful_return_of_single_order(self):
        response = self.tester.get(
            '/api/v1/​​orders​/1',
            headers= dict(Authorization='Bearer '+ self.token),
            content_type='application/json'
                )      
        self.assertEqual(response.status_code, 200)  

    def test_for_no_order_id(self):
        response = self.tester.get(
            '/api/v1/​​orders​/200',
            headers= dict(Authorization='Bearer '+ self.token),
            content_type='application/json'
            )      
        self.assertEqual(response.status_code, 404) 
        self.assertIn(b"The requested order doesn't exist", response.data)    

    def test_no_access_to_non_admin_to_return_single_order(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"ayebare@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":False}),
            content_type='application/json'
        )
        response = self.tester.post(
        '/api/v1/auth/login',
        data=json.dumps({"email":"ayebare@gmail.com", "password":"ayeb"}),
        content_type='application/json', 
        )

        token=json.loads(response.data.decode())["token"]  
        
        response = self.tester.get(
        '/api/v1/​​orders​/1',
        headers= dict(Authorization='Bearer '+ token),
        content_type='application/json'
            )
        self.assertEqual(response.status_code, 401)  
        self.assertIn(b"Admin previledges required to perform this function", response.data)

    def test_for_successful_update_of_order(self):
        response = self.tester.put(
            '/api/v1/​​orders​/1',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"order_status":"new"}),
            content_type='application/json'
                )      
        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'order succesfully updated', response.data)

    def test_for_non_wrong_status_input(self):
        response = self.tester.put(
            '/api/v1/​​orders​/1',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({"order_status":"OLD"}),
            content_type='application/json'
                )      
        self.assertEqual(response.status_code, 400)  
        self.assertIn(b'please add valid status response', response.data)

    def test_for_no_status_response(self):
        response = self.tester.put(
            '/api/v1/​​orders​/1',
            headers= dict(Authorization='Bearer '+ self.token),
            data = json.dumps({}),
            content_type='application/json'
                )      
        self.assertEqual(response.status_code, 400)  
        self.assertIn(b'please add a status response', response.data)

    def test_for_no_access_to_non_admin_to_edit_order_status(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"ayebare@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":False}),
            content_type='application/json'
        )
        response = self.tester.post(
        '/api/v1/auth/login',
        data=json.dumps({"email":"ayebare@gmail.com", "password":"ayeb"}),
        content_type='application/json', 
        )

        token=json.loads(response.data.decode())["token"]  
        
        response = self.tester.put(
        '/api/v1/​​orders​/1',
        headers= dict(Authorization='Bearer '+ token),
        data = json.dumps({"order_status":"cancelled"}),
        content_type='application/json'
            )
        self.assertEqual(response.status_code, 401)  
        self.assertIn(b"Admin previledges required to perform this function", response.data)    


    