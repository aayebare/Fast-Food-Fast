import unittest
import json 
from app import app
from app.models import Database

db=Database()
class TestingEndpoints(unittest.TestCase):
  
    def setUp(self):
        db.create_tables()
        self.tester = app.test_client(self)
        
    def test_valid_user_registration(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"cliff@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"registration was successful", response.data)

    def test_for_empty_password_field(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"aye@gmail.com",
                "password":"", 
                "confirm_password":"ayeb",
                "is_admin":True
                }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add password", response.data)
    
    def test_for_empty_confirm_password_field(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"aye@gmail.com",
                "password":"ayeb", 

                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please confirm-password", response.data)
        print (response.data)

    def test_for_user_passwords_matching(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"aye@gmail.com",
                "password":"ayeb", 
                "confirm_password":"yego",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"passwords do not match, please try again!!", response.data)

    def test_for_empty_username_field(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"" ,
                "email":"aye@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please, add a username", response.data)

    def test_for_empty_user_name_and_email_fields(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add a username and/or email and try again", response.data)

    def test_for_empty_email_field(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"john",
                "email":"",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add an email and try again", response.data)

    def test_for_missing_user_role(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"john",
                "email":"aye@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add a valid account type", response.data)

    def test_for_non_boolean_account_type(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"john",
                "email":"aye@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":5}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add a valid account type", response.data)

    def test_invalid_email_input(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"aye.com",
                "password":"eee", 
                "confirm_password":"eee",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please fill in a valid email address", response.data)    

    def test_for_no_email_field(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add a username and/or email and try again", response.data)

    def test_for_duplicate_emails(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"mark@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"mark@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"this email already exists, please use a different email to signup", response.data)   

    def test_for_succesful_login(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"mark@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({ "email":"mark@gmail.com","password":"ayeb"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User successfully logged in as admin", response.data) 

    def test_for_missing_email_field(self):
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"password":"ayeb"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add an email in order to login", response.data) 

    def test_for_empty_password_field_on_login(self):
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mark@gmail.com","password":""}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add a password in order to login", response.data)     

    def test_for_non_string_in_password(self):
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mark@gmail.com","password":1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"please add a valid password in order to login", response.data) 
  
    def test_email_not_in_database(self):
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"kata@gmail.com", "password":"123"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Incorrect email,please try again or signup!!", response.data) 

    def test_for_wrong_password(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"ayebare" ,
                "email":"mark@gmail.com",
                "password":"ayeb", 
                "confirm_password":"ayeb",
                "is_admin":True}),
            content_type='application/json'
        )
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mark@gmail.com", "password":"16"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Incorrect password, please try again", response.data)   

if __name__ == "__main__":   
    unittest.main() 
