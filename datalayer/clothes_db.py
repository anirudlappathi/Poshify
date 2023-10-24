from .database import dbsession, Base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import colorsys

class Clothes(Base):
    __tablename__ = 'Clothes'
    
    clothes_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    clothing_type = Column(String(255))
    color = Column(String(255))
    is_clean = Column(Boolean)

def create_cloth(user_id, clothing_type, color, is_clean):
    try:
        print(f"Starting Function: {user_id}, {clothing_type}, {color}, {is_clean}")
        new_cloth = Clothes(user_id=user_id, clothing_type=clothing_type, color=color, is_clean=is_clean)
        dbsession.add(new_cloth)
        dbsession.commit()
        print(f"Added to Clothes DB: {user_id} {clothing_type}, {color}, {is_clean}")
        return "WORKING"
    except Exception as e:
        print(f"Create Cloth Error: {e}")
        return f"ERROR: {e}"

###
###
###
##3
### NEW CODE HERE
def get_clothing_type_by_user_id(user_id):
    try:
        clothing_types = dbsession.query(Clothes.clothing_type).filter_by(user_id=user_id).all()
        # Extract clothing types from the query result
        clothing_types = [type[0] for type in clothing_types]
        return clothing_types
    except Exception as e:
        print(f"Get Clothing Types Error: {e}")
        return None




# Read (Select) Users
# def get_all_users():
#     try:
#         select_query = "SELECT * FROM clothes"
#         cursor.execute(select_query)
#         clothes = cursor.fetchall()
#         return clothes
#     except mysql.connector.Error as err:
#         print(f"Get All Users Error: {err}")
#         return None

# def get_user_by_id(user_id):
#     try:
#         select_query = "SELECT * FROM clothes WHERE id = %s"
#         cursor.execute(select_query, (user_id,))
#         user = cursor.fetchone()
#         return user
#     except mysql.connector.Error as err:
#         print(f"Get User By ID Error: {err}")
#         return None

# # Update User Information
# def update_user(user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name):
#     try:
#         update_query = "UPDATE clothes SET user_id = %s username = %s, first_name = %s, last_name = %s, email = %s, phone_number = %s, user_photo_file_name = %s WHERE id = %s"
#         data = (user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name, user_id)
#         cursor.execute(update_query, data)
#         conn.commit()
#         print("User updated successfully.")
#     except mysql.connector.Error as err:
#         print(f"Update User Error: {err}")

# # Delete User
# def delete_user(user_id):
#     try:
#         delete_query = "DELETE FROM clothes WHERE id = %s"
#         cursor.execute(delete_query, (user_id,))
#         conn.commit()
#         print("User deleted successfully.")
#     except mysql.connector.Error as err:
#         print(f"Delete User Error: {err}")