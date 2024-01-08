from .database import dbsession, Base
from sqlalchemy import Column, Integer, String, delete, ForeignKey
from collections import defaultdict

import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

import configparser
config = configparser.ConfigParser()
config.read('config.properties')

if config.get("DEFAULT", "DEVTYPE") == "aws":
   import boto3
   s3 = boto3.client('s3')
   CLOTHING_BUCKET_NAME = "poshify-clothingimages"

class Calendar(Base):
    __tablename__ = 'Calendar'

    outfit_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey('Users.user_id'))
    clothes_id = Column(Integer, ForeignKey('Clothes.clothes_id'))
    dayOfWeek = Column(String(255))
    filepath = Column(String(255))
    outfitType = Column(String(255))
    date = Column(String(6))

# DOOOO THISSS
def create_entry(user_id, clothes_id, dayOfWeek, imagePaths, outfitType, date):
    try:
        for i, image_path in enumerate(imagePaths):
            image_path_modified = image_path.replace('/static/', '')

            new_entry = Calendar(
                user_id=user_id,
                clothes_id=clothes_id[i],
                dayOfWeek=dayOfWeek,
                filepath=image_path_modified,
                outfitType=outfitType,
                date=date
            )
            dbsession.add(new_entry)
        dbsession.commit()
    except Exception as e:
        print(f"create_entry ERROR: {e}")
        dbsession.rollback()
        return f"create_entry ERROR: {e}"

def delete_entry(user_id, dayOfWeek, filepath, outfitType):
    try:
        filepath = filepath.replace('/static/', '')
        delete_query = (
            delete(Calendar)
            .where(
                Calendar.user_id == user_id,
                Calendar.dayOfWeek == dayOfWeek,
                Calendar.filepath == filepath,
                Calendar.outfitType == outfitType
            )
        )
        dbsession.execute(delete_query)
        dbsession.commit()
    except Exception as e:
        print(f"delete_entry ERROR: {e}")
        dbsession.rollback()
        return f"delete_entry ERROR: {e}"


def get_image_paths_per_day(user_id):
    try:
        image_paths_per_day = dbsession.query(Calendar.dayOfWeek, Calendar.outfitType, Calendar.filepath, Calendar.clothes_id) \
            .filter(Calendar.user_id == user_id) \
            .all()
        image_paths_dict = defaultdict(lambda: defaultdict(list))
        all_clothes_id = {}
        set_clothes_ids = set()
        for day, outfit_type, filepath, clothes_id in image_paths_per_day:
            if config.get("DEFAULT", "DEVTYPE") == "aws":
                img_path = filepath
            else:
                img_path = f"{filepath.replace('clothing_images/', config.get('DEFAULT', 'CLOTHING_IMAGES_FILEPATH'))}"
            image_paths_dict[day][outfit_type].append(img_path)
            if day not in all_clothes_id:
                all_clothes_id[day] = []
            all_clothes_id[day].append(clothes_id)
        for value in all_clothes_id.values():
            outfit_id = ""
            for id in value:
                outfit_id += str(id) + ","
            set_clothes_ids.add(outfit_id[:len(outfit_id) - 1])

        return image_paths_dict, set_clothes_ids
    except Exception as e:
        print(f"get_image_paths_per_day ERROR: {e}")
        dbsession.rollback()
        return f"get_image_paths_per_day ERROR: {e}"