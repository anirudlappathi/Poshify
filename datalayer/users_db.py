import mysql.connector
from dotenv import load_dotenv
import os
import sys

global cursor, conn

def create_connection():
    # Establish Database Connection

    load_dotenv()
    password = os.getenv("PASSWORD")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="Poshify"
    )

    # Create a cursor
    cursor = conn.cursor()
    return (cursor, conn)

# Create (Insert) a New User
def create_user(user_id, username, first_name, last_name, email, phone_number, user_photo_file_name):
    try:
        insert_query = "INSERT INTO Users (username, first_name, last_name, email, phone_number, user_photo_file_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (user_id, username, first_name, last_name, email, phone_number, user_photo_file_name)
        cursor.execute(insert_query, data)
        conn.commit()
        print("User created successfully.")
    except mysql.connector.Error as err:
        print(f"Create User Error: {err}")

# Read (Select) Users
def get_all_users():
    try:
        select_query = "SELECT * FROM Users"
        cursor.execute(select_query)
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        print(f"Get All Users Error: {err}")
        return None

def get_user_by_id(user_id):
    try:
        select_query = "SELECT * FROM Users WHERE id = %s"
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Get User By ID Error: {err}")
        return None

# Update User Information
def update_user(user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name):
    try:
        update_query = "UPDATE Users SET user_id = %s username = %s, first_name = %s, last_name = %s, email = %s, phone_number = %s, user_photo_file_name = %s WHERE id = %s"
        data = (user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name, user_id)
        cursor.execute(update_query, data)
        conn.commit()
        print("User updated successfully.")
    except mysql.connector.Error as err:
        print(f"Update User Error: {err}")

# Delete User
def delete_user(user_id):
    try:
        delete_query = "DELETE FROM Users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        conn.commit()
        print("User deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Delete User Error: {err}")

def close_connection():
    cursor.close()
    conn.close()