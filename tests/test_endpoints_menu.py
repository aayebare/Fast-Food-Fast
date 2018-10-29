import unittest
import json 
from app import app
from app.models import Database


db = Database()
class TestingEndpoints(unittest.TestCase):
    def setUp(self):
        db.create_tables()
        self.tester = app.test_client(self)  
        self.response = self.tester.post(
            '/api/v1/auth/signup',
             data=json.dumps({
                "username":"ayebare" ,
                "email":"kab@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        ) 
        self.response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"kab@gmail.com", "password":"ayeb"}),
            content_type='application/json', 
        )

        self.token=json.loads(self.response.data.decode())["token"]
        
    def test_admin_posts_item_in_menu(self):
        self.response = self.tester.post(
           '/api/v1/menu',
            headers= dict(Authorization='Bearer '+ self.token),
            data=json.dumps({"content":"food","detail":"alot of food","price":300.9}),
            content_type='application/json' 
        )
        
        self.assertEqual(self.response.status_code,200)
        self.assertIn(b"Item successfully posted",self.response.data)

    def test_menu_returned(self):
        self.response = self.tester.get(
           '/api/v1/menu',
            headers= dict(Authorization='Bearer '+ self.token),
            content_type='application/json' 
        )
        self.assertEqual(self.response.status_code,200)

    def test_for_empty_content_or_detail_or_price_fields(self):
        self.response = self.tester.post('/api/v1/menu',
            headers= dict(Authorization='Bearer '+ self.token),
            data=json.dumps({}),
            content_type='application/json'
            )    
        self.assertEqual(self.response.status_code, 400)
        self.assertIn(b"Please add content or detail or price fields", self.response.data)    

    def test_for_empty_price_field(self):
        self.response = self.tester.post(
            'api/v1/menu',
            headers= dict(Authorization ='Bearer '+ self.token),
            data=json.dumps({"content":"meat","detail":"beef","price":""}),
            content_type = 'application/json'
        )   
        self.assertEqual(self.response.status_code,400)
        self.assertIn(b"Please add a unit price", self.response.data) 

    def test_for_empty_content_field(self):
        self.response = self.tester.post(
            'api/v1/menu',
            headers = dict(Authorization ='Bearer '+ self.token),
            data = json.dumps({"content":"", "detail":"all the above", "price":400.9}),
            content_type = 'application/json'
            )
        self.assertEqual(self.response.status_code,400)
        self.assertIn(b'Please add value in the content field', self.response.data)   

    def test_for_error_for_non_admin_post_menu(self):
        self.response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"an@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":False}),
            content_type='application/json'
            )
        self.response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"an@gmail.com", "password":"ayeb"}),
            content_type='application/json', 
        )

        self.token=json.loads(self.response.data.decode())["token"]
        
        self.response = self.tester.post(
            '/api/v1/menu',
            headers= dict(Authorization='Bearer '+ self.token),
            content_type='application/json'
                )
        self.assertEqual(self.response.status_code, 401)  
        self.assertIn(b"Admin previledges required to perform this function",self.response.data)
            




    
    # def test_get_non_existing_orders(self):
    #     self.tester.post(
    #         '/api/v1/auth/signup',
    #         data=json.dumps({
    #             "username":"ayebare" ,
    #             "email":"t@gmail.com",
    #             "password":"ayeb", 
    #             "confirm password":"ayeb",
    #             "is_admin":False}),
    #         content_type='application/json'
    #         )
    #     response1 = self.tester.post(
    #         '/api/v1/auth/login',
    #         data=json.dumps({"email":"t@gmail.com", "password":"ayeb"}),
    #         content_type='application/json', 
    #     )
    #     #raise Exception(response1)
    #     data = json.loads(response1.data.decode())
    #     token = data.get('token')
      

    #     response2 = self.tester.get('/api/v1/orders',
    #     headers=({'token': token}),
    #     content_type='application/json')
       
    #     self.assertEqual(response2.status_code, 404)
    