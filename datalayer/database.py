# sets up the connection to the db

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("PASSWORD")

DATABASE_URL = f'mysql+mysqlconnector://root:{password}@localhost/Poshify'
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
dbsession = Session()

Base = declarative_base()