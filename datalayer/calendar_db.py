from .database import dbsession, Base
from sqlalchemy import Column, Integer, String, delete
from collections import defaultdict

class Calendar(Base):
    __tablename__ = 'Calendar'

    user_id = Column(String(255), primary_key=True)
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
    print("DELTE ENTRY FUNCTION RAN")


    result = dbsession.execute(delete_query)
    dbsession.commit()


def get_image_paths_per_day(user_id):
    try:
        # Query to retrieve image file paths and outfit types per day for the given user ID
        image_paths_per_day = dbsession.query(Calendar.dayOfWeek, Calendar.outfitType, Calendar.filepath) \
            .filter(Calendar.user_id == user_id) \
            .all()

        # Process the retrieved data as needed
        image_paths_dict = defaultdict(lambda: defaultdict(list))
        for day, outfit_type, filepath in image_paths_per_day:
            image_paths_dict[day][outfit_type].append(filepath)

        return image_paths_dict

    except Exception as e:
        print(f"Error retrieving image paths: {str(e)}")
        return None