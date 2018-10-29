import psycopg2
import os 
from app import env
import config
class Database:
    def __init__(self):  
        

        if env == "config.DevelopmentConfig":       
            conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="ayek",
            dbname="fastfood",
                                ) 

            self.conn = conn
            self.c = self.conn.cursor()
            self.conn.autocommit = True

      
        elif env == "config.ProductionConfig":
            conn = psycopg2.connect(
            host='ec2-75-101-138-26.compute-1.amazonaws.com',
            user='umbttjpzbhxvjb',
            password=
            '124c47c1a818fff126c0e0c7f54d7cd88130c5364f895b9814c4c98fb266299f',
            dbname="d3rkfo13e0h1h0",
            port='5432'
            )
            self.conn = conn
            self.c = self.conn.cursor()
            self.conn.autocommit = True

        else: 
            #env == "config.TestingConfig":
            conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='ayek',
            dbname='testdb'
            )
            self.conn = conn
            self.c = self.conn.cursor()
            self.conn.autocommit = True

        # self.conn.autocommit = True
       # c = self.conn.cursor()
        
    def create_tables(self):
        
        commands=(
            '''CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY NOT NULL,
                username VARCHAR(50),
                email VARCHAR(50),
                password VARCHAR(100),
                is_admin BOOLEAN NOT NULL
            )'''
            ,
            '''CREATE TABLE IF NOT EXISTS menu(
                user_id INTEGER,
                item_id SERIAL PRIMARY KEY NOT NULL,
                content VARCHAR(250),
                detail VARCHAR(250),
                price FLOAT,
                FOREIGN KEY (user_id)
                REFERENCES users (user_id) ON DELETE
                CASCADE
            )'''  
            ,
            '''CREATE TABLE IF NOT EXISTS orders(
                user_id INTEGER,
                item_id INTEGER,
                order_id SERIAL PRIMARY KEY,
                date_post VARCHAR(50),
                content VARCHAR(250),
                order_status VARCHAR(50),
                FOREIGN KEY (user_id)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (item_id) REFERENCES menu (item_id)
                ON DELETE CASCADE
                )''' 
            )
        for command in commands:
            self.c.execute(command)
    '''delete tables from the database'''
    def delete_tables(self):
        command = "DROP TABLE users, orders, menu"
        self.c.execute(command)