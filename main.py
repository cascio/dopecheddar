from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import soundcloud_tools
import track_data

# set soundcloud_user_id to target and num_tracks to retreive
soundcloud_user_id = '50163285' # dopecheddar's account id ;)
num_tracks = 2

# creating a SQLAlchemy engine to connect to a postgreSQL database
db_string = environ['DOPECHEDDAR_DB'] # environment variable contains location of postgres database
db = create_engine(db_string)
Session = sessionmaker(db)  
session = Session()

recent_tracks = soundcloud_tools.get_recent_favorites(soundcloud_user_id, num_tracks)
converted_recent_tracks = soundcloud_tools.convert_to_SoundcloudTrack(recent_tracks)

for track in converted_recent_tracks:  
    if track_data.track_already_archived(session, track.track_id):
        print("Track Is Already In Database")
    else:
        print("Track Is Not Yet Saved To Database")