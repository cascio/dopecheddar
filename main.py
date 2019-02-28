from os import environ
from soundcloud_tools import get_recent_favorites
from tumblr import postTrackToTumblr
from track_data import archive_track, track_already_archived
from sys import exit

def setEnvironment():
    required_env_vars = {
        'DOPECHEDDAR_DB': None,
        'SOUNDCLOUD_CLIENT_ID': None,
        'SOUNDCLOUD_SECRET_ID': None,
        'TUMBLR_CLIENT_KEY': None,
        'TUMBLR_CLIENT_SECRET': None,
        'TUMBLR_RESOURCE_OWNER_KEY': None,
        'TUMBLR_RESOURCE_OWNER_SECRET': None,
        'TUMBLR_POST_URL': None,
    }

    for var in required_env_vars:
        if var in environ:
            required_env_vars[var] = environ[var]
        else:
            print(f"Environment Variable: {var} not set. Create the environment variable and try again.")
            exit()
    return required_env_vars

def main():
    configs = setEnvironment()

    # set soundcloud_user_id to target and num_tracks to retreive
    soundcloud_user_id = '50163285' # dopecheddar's account id ;)
    num_tracks = 1

    recent_tracks = get_recent_favorites(configs['SOUNDCLOUD_CLIENT_ID'], configs['SOUNDCLOUD_SECRET_ID'], soundcloud_user_id, num_tracks)

    for track in recent_tracks:  
        if track_already_archived(configs['DOPECHEDDAR_DB'], track.track_id):
            print("Track Is Already In Database")
            pass
        else:
            print("Track Has Not Yet Been Saved To Database......Saving Now")
            postTrackToTumblr(configs['TUMBLR_CLIENT_KEY'], configs['TUMBLR_CLIENT_SECRET'], configs['TUMBLR_RESOURCE_OWNER_KEY'], configs['TUMBLR_RESOURCE_OWNER_SECRET'], configs['TUMBLR_POST_URL'], track)
            archive_track(configs['DOPECHEDDAR_DB'], track)
            print("Track Archived Successfully")

if __name__ == "__main__":
    main()