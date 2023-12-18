from .database import dbsession, Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'Users'

    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(20))
    user_photo_file_name = Column(String(255))

def create_user(username, first_name, last_name, email, phone_number, user_photo_file_name):
    user_with_same_email = dbsession.query(User).filter_by(email=email).first()
    user_with_same_username = dbsession.query(User).filter_by(username=username).first()

    if user_with_same_email:
        return 'EMAIL IN USE'
    if user_with_same_username:
        return 'USERNAME IN USE'
    
    try:
        print("Starting Function: ", username, first_name, last_name, email, phone_number, user_photo_file_name)
        new_user = User(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            phone_number=phone_number, 
            user_photo_file_name=user_photo_file_name
        )
        dbsession.add(new_user)
        dbsession.commit()
        print(f"Added to User DB: ", username, first_name, last_name, email, phone_number, user_photo_file_name)
        return 'CREATED'
    except Exception as e:
        print(f"Create User Error: {e}")
        return 'ERROR'

def get_all_users():
    try:
        users = dbsession.query(User).all()
        return users
    except Exception as e:
        print(f"Get All Users Error: {e}")
        return f"ERROR: {e}"

def get_user_id_by_username(username):
    try:
        user = dbsession.query(User).filter_by(username=username).first()
        return user.user_id
    except Exception as e:
        print(f"Get User By Username Error: {e}")
        return f"ERROR: {e}"
    
def get_user_by_id(user_id):
    try:
        user = dbsession.query(User).filter_by(id=user_id).first()
        return user
    except Exception as e:
        print(f"Get User By ID Error: {e}")
        return f"ERROR: {e}"

def update_user(user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name):
    try:
        user = dbsession.query(User).filter_by(id=user_id).first()
        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.phone_number = new_phone_number
        user.user_photo_file_name = new_user_photo_file_name
        dbsession.commit()
        print("User updated successfully.")
    except Exception as e:
        print(f"Update User Error: {e}")

def delete_user(user_id):
    try:
        user = dbsession.query(User).filter_by(id=user_id).first()
        dbsession.delete(user)
        dbsession.commit()
        print("User deleted successfully.")
    except Exception as e:
        print(f"Delete User Error: {e}")

def close_connection():
    dbsession.close()