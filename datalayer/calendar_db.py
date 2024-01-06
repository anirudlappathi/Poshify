from .database import dbsession, Base
from sqlalchemy import Column, Integer, String, delete
from collections import defaultdict

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
    user_id = Column(String(255))
    dayOfWeek = Column(String(255))
    filepath = Column(String(255))
    outfitType = Column(String(255))

def create_entry(user_id, dayOfWeek, imagePaths, outfitType):
    try:
        for image_path in imagePaths:
            image_path_modified = image_path.replace('/static/', '')

            new_entry = Calendar(
                user_id=user_id,
                dayOfWeek=dayOfWeek,
                filepath=image_path_modified,
                outfitType=outfitType
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
        image_paths_per_day = dbsession.query(Calendar.dayOfWeek, Calendar.outfitType, Calendar.filepath) \
            .filter(Calendar.user_id == user_id) \
            .all()
        image_paths_dict = defaultdict(lambda: defaultdict(list))
        for day, outfit_type, filepath in image_paths_per_day:
            print(filepath)
            if config.get("DEFAULT", "DEVTYPE") == "aws":
                #url = s3.generate_presigned_url('get_object', Params={'Bucket': CLOTHING_BUCKET_NAME, 'Key': f'clothing_images/{item.clothingimg_filepath}'}, ExpiresIn=3600)
                #img_path = s3.generate_presigned_url('get_object', Params={'Bucket': CLOTHING_BUCKET_NAME, 'Key': f'{filepath}'}, ExpiresIn=3600)
                #print("FILE PATH IN GET IMAGE PATHS PER DAY: ", filepath)
                img_path = filepath
            else:
                img_path = f"{filepath.replace('clothing_images/', config.get('DEFAULT', 'CLOTHING_IMAGES_FILEPATH'))}"
            image_paths_dict[day][outfit_type].append(img_path)

        return image_paths_dict

    except Exception as e:
        print(f"get_image_paths_per_day ERROR: {e}")
        dbsession.rollback()
        return f"get_image_paths_per_day ERROR: {e}"