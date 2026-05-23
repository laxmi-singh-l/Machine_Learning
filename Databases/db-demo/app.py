import sys
from typing import Any
from dbhelper import DBHelper

class flipcart:
    
    def __init__(self) :
        self.dbhelper = DBHelper()

        # self.menu() is called in the constructor to display the menu options when an instance of the flipcart class is created.
        # connect to the database and create a cursor object to execute SQL queries.
        
        self.menu()

    def menu(self):

        user_input = input("""
              1. Enter 1 to register
              2. Enter 2 to login
              3. Exit
              """)    
        

        if user_input == '1':
            self.register() 
        elif user_input == '2':
            self.login()   
        else:
            sys.exit(1000)     

    def register(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, password)

        self.dbhelper.cursor.execute(query, values)
        self.dbhelper.conn.commit()

        print("User registered successfully!")

    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)

        self.dbhelper.cursor.execute(query, values)
        user = self.dbhelper.cursor.fetchone()

        if user:
            print(f"Welcome!")
        else:
            print("Invalid email or password.")    
