import sys
import mysql.connector



class DBHelper:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="machine_learning",
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print("Database connection failed")
            sys.exit(1)
        else:
            print("Connection successful")
print("DBHelper initialized successfully")
