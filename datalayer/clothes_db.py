from algorithm import color_algo
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from .database import dbsession, Base
import os
# import logging

# # Set the logging level to suppress SQLAlchemy logs (INFO level)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

class Clothes(Base):
    __tablename__ = 'Clothes'
    
    clothes_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey('Users.user_id'))
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

        new_cloth = Clothes(user_id=user_id, clothing_name=clothing_name, clothing_type=clothing_type, is_clean=is_clean, hue=hue, saturation=saturation, value=value, tone=tone, colortemp=colortemp, clothingimg_filepath = clothingimg_filepath)

        dbsession.add(new_cloth)
        dbsession.commit()
        return "Cloth created successfully"
    except Exception as e:
        print(f"Create Cloth Error: {e}")
        return f"ERROR: {e}"

def get_clothing_name_image_id_by_user_id(user_id):  # returns clothing img file as well
    try:
        clothing = dbsession.query(Clothes).filter_by(user_id=user_id).all()
        clothing_data = []
        for item in clothing:
            clothing_data.append((
                item.clothing_name,
                os.path.join("clothing_images", item.clothingimg_filepath),
                item.clothes_id,
                item.is_clean  # Assuming is_clean is a field in the Clothes model
            ))
        return clothing_data
    except Exception as e:
        print(f"Get Clothing Data Error: {e}")
        return None


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
    
def update_clothing_name_by_identifier(identifier, updated_text, user_id):
    try:
        cloth_item = dbsession.query(Clothes).filter_by(clothing_name=identifier, user_id=user_id).first()

        if cloth_item:
            cloth_item.clothing_name = updated_text
            dbsession.commit()
            return "Clothing name updated successfully"
        else:
            return "Clothing item not found or doesn't belong to the user"
    except Exception as e:
        print(f"Update Clothing Name Error: {e}")
        return f"ERROR: {e}"

def delete_clothing_by_id(clothes_id, user_id):
    try:
        cloth_item = dbsession.query(Clothes).filter(Clothes.clothes_id==clothes_id, Clothes.user_id==user_id).first()

        if cloth_item:
            dbsession.delete(cloth_item)
            dbsession.commit()
            return "Clothing deleted successfully"
        else:
            return "Clothing item not found or doesn't belong to the user"
    except Exception as e:
        print(f"Delete Clothing Error: {e}")
        return f"ERROR: {e}"
    
def get_clothing_url_by_id(clothes_id, user_id):
    try:
        print(clothes_id, user_id)
        clothing_url = dbsession.query(Clothes).filter(Clothes.clothes_id==clothes_id, Clothes.user_id==user_id).first()
        return clothing_url.clothingimg_filepath
    except Exception as e:
        print(f"GET CLOTHING URL BY ID Clothing Error: {e}")
        return f"ERROR: {e}"
    
def is_clothing_name_by_id(clothes_name, user_id):
    try:
        name_exists = dbsession.query(Clothes).filter(Clothes.user_id == user_id, func.trim(Clothes.clothing_name) == clothes_name.strip()).first()
        print('a',name_exists)
        print('b',bool(name_exists))
        return bool(name_exists)
    except Exception as e:
        print(f"CHECK CLOTHING NAME AND ID ERROR: {e}")
        return f"ERROR: {e}"

def update_cleanliness_status(clothid, new_status):
    try:
        print("clothid in function: ", clothid)
        print("new status in function: ", new_status)
        clothing_item = dbsession.query(Clothes).filter_by(clothes_id=clothid).first()
        print("clothing item; ", clothing_item)
        if clothing_item:
            if new_status.lower() == 'clean':
                clothing_item.is_clean = 1  # Set as 1 (True)
                print("set to clean")
            elif new_status.lower() == 'dirty':
                clothing_item.is_clean = 0  # Set as 0 (False)
                print("Set to dirty")

            dbsession.commit()
            return f"Updated cleanliness status of clothing ID {clothid} to {new_status.capitalize()}"
        else:
            return f"Clothing item with ID {clothid} not found"
    except Exception as e:
        return f"Error: {e}"
