from .database import dbsession, Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(String(255), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(20))
    user_photo_file_name = Column(String(255))

def create_user(user_id, username, password, first_name, last_name, email, phone_number, user_photo_file_name):
    user_with_same_email = dbsession.query(Users).filter_by(email=email).first()
    user_with_same_username = dbsession.query(Users).filter_by(username=username).first()
    if user_with_same_email:
        return 'EMAIL IN USE'
    if user_with_same_username:
        return 'USERNAME IN USE'
    
    try:
        new_user = Users(
            user_id=user_id,
            username=username, 
            password=password,
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            phone_number=phone_number, 
            user_photo_file_name=user_photo_file_name
        )
        dbsession.add(new_user)
        dbsession.commit()
        return get_user_id_by_username(username)
    except Exception as e:
        print(f"Create Users Error: {e}")
        return 'CREATE USER ERROR'

def get_all_users():
    try:
        users = dbsession.query(Users).all()
        return users
    except Exception as e:
        print(f"Get All Users Error: {e}")
        return f"ERROR: {e}"

def get_user_id_by_username(username):
    try:
        user = dbsession.query(Users).filter_by(username=username).first()
        print('userid: ', user)
        return user.user_id
    except Exception as e:
        print(f"Get Users By Username Error: {e}")
        return None

def get_user_by_id(user_id):
    try:
        user = dbsession.query(Users).filter_by(id=user_id).first()
        return user
    except Exception as e:
        print(f"Get Users By ID Error: {e}")
        return f"ERROR: {e}"

def update_user(user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name):
    try:
        user = dbsession.query(Users).filter_by(id=user_id).first()
        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.phone_number = new_phone_number
        user.user_photo_file_name = new_user_photo_file_name
        dbsession.commit()
        print("Users updated successfully.")
    except Exception as e:
        print(f"Update Users Error: {e}")

def delete_user(user_id):
    try:
        user = dbsession.query(Users).filter_by(id=user_id).first()
        dbsession.delete(user)
        dbsession.commit()
        print("Users deleted successfully.")
    except Exception as e:
        print(f"Delete Users Error: {e}")

def close_connection():
    dbsession.close()