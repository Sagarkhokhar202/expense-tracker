import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sagarkhokhar202@",
        database="expense_tracker"
    )
