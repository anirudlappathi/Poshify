from .database import dbsession, Base
from sqlalchemy import Column, Integer, String

class Calendar(Base):
    __tablename__ = 'Calendar'

    user_id = Column(String(255), primary_key=True)
    dayOfWeek = Column(String(255))
    filepath = Column(String(255))

def create_entry(user_id, dayOfWeek, imagePaths):
    for image_path in imagePaths:
        # Remove '/static/' from the image path
        image_path_modified = image_path.replace('/static/', '')

        new_entry = Calendar(
            user_id=user_id,
            dayOfWeek=dayOfWeek,
            filepath=image_path_modified
        )
        dbsession.add(new_entry)
        dbsession.commit()

    print("CREATE_ENTRY FOR CALENDAR RAN")



def get_image_paths_per_day(user_id):
    try:
        # Query to retrieve image file paths per day for the given user ID
        image_paths_per_day = dbsession.query(Calendar.dayOfWeek, Calendar.filepath) \
            .filter(Calendar.user_id == user_id) \
            .all()

        # Process the retrieved data as needed
        image_paths_dict = {}
        for day, filepath in image_paths_per_day:
            if day not in image_paths_dict:
                image_paths_dict[day] = []
            image_paths_dict[day].append(filepath)

        return image_paths_dict

    except Exception as e:
        print(f"Error retrieving image paths: {str(e)}")
        return None