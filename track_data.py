from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

# using declarative_base() to take advantage of SQLAlchemy's ORM capabilities
Base = declarative_base()

# SoundCloudTrack object; subclassing 'Base" for SQLAlchemy.
class SoundcloudTrack(Base):
    __tablename__ = 'SoundcloudTracks'
    name = Column(String)
    track_id = Column(String, primary_key=True)
    url = Column(String)
    genre = Column(String)
    label = Column(String)
    tag_list = Column(String)
    def __init__(self, name, track_id, url, genre, label, tag_list):
        self.name = name
        self.track_id = str(track_id)
        self.url = url
        self.genre = genre
        self.label = label
        self.tag_list = tag_list

# creating a SQLAlchemy engine and session to connect to and interact with postgreSQL database
def get_database_session(db_string):
    db_string = db_string # location of postgres database
    db = create_engine(db_string)
    Session = sessionmaker(db)  
    session = Session()
    return session

# checks if the track is unique compared to the Postgres database using SQLAlchemy
def track_already_archived(db_string, track_id):
    session = get_database_session(db_string)
    ret = session.query(exists().where(SoundcloudTrack.track_id==track_id)).scalar()
    return ret

def archive_track(db_string, track):
    session = get_database_session(db_string)
    session.add(track)
    session.commit()

# creates tables based on SQLAlchemy's ORM if they do not exist; no longer needed for me
#Base.metadata.create_all(db)