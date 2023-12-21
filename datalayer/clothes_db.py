from .database import dbsession, Base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import colorsys
from algorithm import color_algo


class Clothes(Base):
    __tablename__ = 'Clothes'
    
    clothes_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    clothing_name = Column(String(255))
    clothing_type = Column(String(255))
    is_clean = Column(Boolean)
    hue = Column(Integer)
    saturation = Column(Integer)
    value = Column(Integer)
    tone = Column(Integer)
    colortemp = Column(Integer)
    clothingimg_filepath = Column(String(255))

def create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value, clothingimg_filepath):
    try:
        tone = color_algo.GetTone((int(saturation), int(value)))
        colortemp = color_algo.GetColorTemp(hue)

        new_cloth = Clothes(user_id=user_id, clothing_name=clothing_name, clothing_type=clothing_type, is_clean=is_clean, hue=hue, saturation=saturation, value=value, tone=tone, colortemp=colortemp, clothingimg_filepath = clothingimg_filepath + ".jpg")

        dbsession.add(new_cloth)
        dbsession.commit()
        return "Cloth created successfully"
    except Exception as e:
        print(f"Create Cloth Error: {e}")
        return f"ERROR: {e}"

def get_clothing_type_by_user_id(user_id): #returns clothing img file as well
    try:
        clothing_data = dbsession.query(Clothes.clothing_name, Clothes.clothingimg_filepath).filter_by(user_id=user_id).all()
        clothing_dict = {item[0]: item[1] for item in clothing_data}
        return clothing_dict
    except Exception as e:
        print(f"Get Clothing Data Error: {e}")
        return None

'''
def get_clothing_type_by_user_id(user_id): #original get clothing function
    try:
        clothing_types = dbsession.query(Clothes.clothing_name).filter_by(user_id=user_id).all()
        return clothing_types
    except Exception as e:
        print(f"Get Clothing Types Error: {e}")
        return None
'''
def get_clothing_by_type(user_id, clothing_type):
    try:
        names = dbsession.query(Clothes.clothing_name).filter_by(user_id=user_id, clothing_type=clothing_type).all()
        hues = dbsession.query(Clothes.hue).filter_by(user_id=user_id, clothing_type=clothing_type).all()
        saturation = dbsession.query(Clothes.saturation).filter_by(user_id=user_id, clothing_type=clothing_type).all()
        value = dbsession.query(Clothes.value).filter_by(user_id=user_id, clothing_type=clothing_type).all()
        clothes = []
        for i in range(len(hues)):
            clothes.append((names[i][0], hues[i][0], saturation[i][0], value[i][0]))

        return clothes
    except:
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

