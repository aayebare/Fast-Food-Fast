import psycopg2
from app.models import Database
from app import env

db = Database()


class User:
    def __init__(self, username, email, password, is_admin):
        #super().__init__()
        
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    '''add a user'''

    def add_user(self):
        command = """INSERT INTO users (email, username, password,is_admin)
        VALUES (%s, %s, %s, %s)"""
        db.c.execute(command,
                     (self.email, self.username, self.password, self.is_admin))

    '''check for duplicate email in database'''

    def check_duplicate(self):
        command = """SELECT email FROM users WHERE email = %s"""
        db.c.execute(command, (self.email, ))
        value = db.c.fetchone()
        return value
    def check_admin(self):
        command = """SELECT is_admin FROM users WHERE email = %s"""
        db.c.execute(command, (self.email, ))
        value = db.c.fetchone()
        return value    
        

    '''login user'''

    def login_user(self):
        command = "SELECT user_id,password FROM users WHERE email = %s"
        db.c.execute(command, (self.email, ))
        value = db.c.fetchone()
        return value

    '''check user role'''

    @staticmethod
    def check_user_role(user_id):
        command = "SELECT is_admin FROM users where user_id = " + str(user_id)
        #command = "SELECT is_admin FROM users where user_id = %s"
        # command = "SELECT is_admin FROM users WHERE user_id = '{}'".format(
        #     user_id)
        db.c.execute(command,)
        value = db.c.fetchone()
        print (value)
        return value
