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

# checks if the track is unique compared to the Postgres database using SQLAlchemy
def track_already_archived(session, track_id):
    ret = session.query(exists().where(SoundcloudTrack.track_id==track_id)).scalar()
    return ret

# creates tables based on SQLAlchemy's ORM if they do not exist
#Base.metadata.create_all(db)