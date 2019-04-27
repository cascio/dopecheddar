'''Postgres database functionality with SQLAlchemy ORM capabilities'''

import re
from sqlalchemy import create_engine, Boolean, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

Base = declarative_base()

class SoundcloudTrack(Base):
    '''Custom SoundcloudTrack object and Postgres database schema'''
    __tablename__ = 'SoundcloudTracks'
    name = Column(String)
    track_id = Column(String, primary_key=True)
    url = Column(String)
    genre = Column(String)
    label = Column(String)
    tag_list = Column(String)
    posted_to_tumblr = Column(Boolean, default=False)
    posted_to_twitter = Column(Boolean, default=False)
    def __init__(self, name, track_id, url, genre, label, tag_list):
        self.name = name
        self.track_id = str(track_id)
        self.url = url
        self.genre = genre
        self.label = label
        self.tag_list = generate_track_tags(tag_list)
        self.posted_to_tumblr = False
        self.posted_to_twitter = False

def get_database_session(db_string):
    '''Create SQLAlchemy engine and session to connect to and interact with Postgres database'''
    db_string = db_string # location of postgres database
    database = create_engine(db_string)
    Session = sessionmaker(database)
    session = Session()
    return session

def track_already_archived(db_string, track_id):
    '''Check if track has already been archived to Postgres database'''
    session = get_database_session(db_string)
    ret = session.query(exists().where(SoundcloudTrack.track_id == track_id)).scalar()
    return ret

def archive_track(db_string, track):
    '''Add track to Postgres database and set posted_to_tumblr to True'''
    track.posted_to_tumblr = True
    session = get_database_session(db_string)
    session.add(track)
    session.commit()

def generate_track_tags(tag_list):
    '''Generate a tag list from retreived soundcloud string. Returns string seperated by commas'''
    do_not_tag = ["exclusive", "premiere", "ep", "lp", "first floor premiere", ]
    # Strings that should always be tagged
    always_tag = ["dopecheddar", "electronic music", "electronic", "music"]
    # Convert characters to lowercase for duplicate catching
    tag_list = tag_list.lower()
    # Identify soudcloud post two-word tags and start final tag list
    final_tags = re.findall('"(.*?)"', tag_list)
    # Remove two-word tags from tag list retrieved from soundcloud post
    for quoted_tag in final_tags:
        tag_list = tag_list.replace(f'"{quoted_tag}"', '')
    # Create list from string of tags retrieved from soundcloud post
    tag_list = tag_list.split()
    # Combining final tag list and removing items that should never be tagged
    final_tags = list(set(final_tags + tag_list + always_tag) - set(do_not_tag))
    # Tumblr requires tags to be a string with each tag seperated by commas
    final_tags = ", ".join(final_tags)
    return final_tags

# creates tables based on SQLAlchemy's ORM if they do not exist; no longer needed for me
#Base.metadata.create_all(database)
