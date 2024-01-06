from algorithm import color_algo
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from .database import dbsession, Base
import os
import logging

import configparser
config = configparser.ConfigParser()
config.read('config.properties')

# Set the logging level to suppress SQLAlchemy logs (INFO level)
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

if config.get("DEFAULT", "DEVTYPE") == "aws":
   import boto3
   s3 = boto3.client('s3')
   CLOTHING_BUCKET_NAME = "poshify-clothingimages"

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
            if config.get("DEFAULT", "DEVTYPE") == "aws":
                url = s3.generate_presigned_url('get_object', Params={'Bucket': CLOTHING_BUCKET_NAME, 'Key': f'clothing_images/{item.clothingimg_filepath}'}, ExpiresIn=3600)
            else:
                url = f"{config.get('DEFAULT', 'CLOTHING_IMAGES_FILEPATH')}{item.clothingimg_filepath}"
            clothing_data.append((
                item.clothes_id,
                item.clothing_type,
                item.clothing_name,
                item.is_clean,
                item.hue,
                item.saturation,
                item.value,
                url
            ))
        return clothing_data
    except Exception as e:
        print(f"Get Clothing Data Error: {e}")
        return None


def get_clothing_by_type(user_id, clothing_type, folder="CLOTHING_IMAGES_FILEPATH"):
    try:

        data = dbsession.query(Clothes.hue, Clothes.saturation, Clothes.value, Clothes.clothing_name, Clothes.clothingimg_filepath).filter_by(user_id=user_id, clothing_type=clothing_type).all()


        clothes = []
        for item in data:
            if config.get("DEFAULT", "DEVTYPE") == "aws":
                url = s3.generate_presigned_url('get_object', Params={'Bucket': CLOTHING_BUCKET_NAME, 'Key': f'clothing_images/{item.clothingimg_filepath}'}, ExpiresIn=3600)
            else:
                url = f"{config.get('DEFAULT', folder)}{item.clothingimg_filepath}"
            cloth_data = (item.hue, item.saturation, item.value, item.clothing_name, url)
            clothes.append(cloth_data)

        return clothes
    except Exception as e:
        print(f"Get Clothing Types Error: {e}")
        return None
    
def update_clothing_name_by_clothing_name(clothing_name, updated_text, user_id):
    try:
        cloth_item = dbsession.query(Clothes).filter_by(clothing_name=clothing_name, user_id=user_id).first()

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
    
def has_clothing_name_by_id(clothes_name, user_id):
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

def get_image_paths_by_name(user_id, clothing_name):
    try:
        # Query the database to fetch the clothingimg_filepath based on user_id and clothing_name
        clothing_item = dbsession.query(Clothes).filter_by(user_id=user_id, clothing_name=clothing_name).first()

        if clothing_item:
            return 'clothing_images/' + clothing_item.clothingimg_filepath
        else:
            return None  # Or handle the case where the clothing item is not found
    except Exception as e:
        print(f"Error fetching image path: {e}")
        return None  # Handle exceptions gracefully
    