from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

class Clothes(Base):
    __tablename__ = 'clothes'
    clothes_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    clothing_type = Column(String(255))
    color = Column(String(255))
    is_clean = Column(Boolean)

load_dotenv()
password = os.getenv("PASSWORD")

DATABASE_URL = f'mysql+mysqlconnector://root:{password}@localhost/Poshify'
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def create_cloth(clothing_type, color, is_clean):
    try:
        new_cloth = Clothes(clothing_type=clothing_type, color=color, is_clean=is_clean)
        session.add(new_cloth)
        session.commit()
        print(f"Added to Clothes DB: {clothing_type}, {color}, {is_clean}")
        return True
    except Exception as e:
        print(f"Create Cloth Error: {e}")

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

# def close_connection():
#     cursor.close()
#     conn.close()