from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
import re

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
        self.tag_list = generate_track_tags(tag_list)

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

def generate_track_tags(tag_list):
    # What should never be a tag
    do_not_tag = ["exclusive", "premiere", "ep", "lp", "first floor premiere", ]
    always_tag = ["dopecheddar", "electronic music", "electronic", "music"]
    # Convert all characters in tag list from soundcloud post to lowercase to catch duplicates
    tag_list = tag_list.lower()
    # Identify two word tags from soundcloud post and start a final tag list
    final_tags = re.findall('"(.*?)"', tag_list)
    # Remove two word tags from soundcloud post from soundcloud post track list
    for quoted_tag in final_tags:
        tag_list = tag_list.replace(f'"{quoted_tag}"', '')
    # Create list by splitting the soundcloud post string tag list at spaces
    tag_list = tag_list.split()
    final_tags = list(set(final_tags + tag_list + always_tag) - set(do_not_tag))
    final_tags = ", ".join(final_tags)
    return final_tags

# creates tables based on SQLAlchemy's ORM if they do not exist; no longer needed for me
#Base.metadata.create_all(db)