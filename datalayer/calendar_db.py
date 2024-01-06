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
    # Check for existing entries for the user on the specified day
    print("DAY OF WEEK ", dayOfWeek)

    # Create new entries
    for image_path in imagePaths:
        # Remove '/static/' from the image path
        image_path_modified = image_path.replace('/static/', '')

        new_entry = Calendar(
            user_id=user_id,
            dayOfWeek=dayOfWeek,
            filepath=image_path_modified,
            outfitType=outfitType
        )
        dbsession.add(new_entry)
    dbsession.commit()

    print("CREATE_ENTRY FOR CALENDAR RAN")

def delete_entry(user_id, dayOfWeek, filepath, outfitType):
    # Construct a list of filepaths to match against
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
    


    result = dbsession.execute(delete_query)
    dbsession.commit()
    print("DELETE ENTRY FUNCTION RAN")


def get_image_paths_per_day(user_id):
    try:
        # Query to retrieve image file paths and outfit types per day for the given user ID
        image_paths_per_day = dbsession.query(Calendar.dayOfWeek, Calendar.outfitType, Calendar.filepath) \
            .filter(Calendar.user_id == user_id) \
            .all()

        # Process the retrieved data as needed
        image_paths_dict = defaultdict(lambda: defaultdict(list))
        for day, outfit_type, filepath in image_paths_per_day:
            if config.get("DEFAULT", "DEVTYPE") == "aws":
                img_path = s3.generate_presigned_url('get_object', Params={'Bucket': CLOTHING_BUCKET_NAME, 'Key': f'clothing_images/{filepath}'}, ExpiresIn=3600)
            else:
                img_path = f"{filepath.replace('clothing_images/', config.get('DEFAULT', 'CLOTHING_IMAGES_FILEPATH'))}"
            image_paths_dict[day][outfit_type].append(img_path)

        return image_paths_dict

    except Exception as e:
        print(f"Error retrieving image paths: {str(e)}")
        return None