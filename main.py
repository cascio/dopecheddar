'''Main music content distribution functionality'''

from os import environ
from soundcloud_tools import get_recent_favorites
from track_data import archive_track, track_already_archived
from tumblr import postTrackToTumblr

def set_environment():
    '''Retreives configurations from enviroment variables, if properly set'''
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
            print(f"Environment Variable: {var} not set. Set the env var  and try again.")
            exit()
    return required_env_vars

def main():
    '''Just do it!'''
    print("-----TURNING UP-----")
    print("")
    configs = set_environment()

    # set soundcloud_user_id to target and num_tracks to retreive
    soundcloud_user_id = '50163285' # dopecheddar's account id ;)
    num_tracks = 10

    print(f"Retreiving {num_tracks} tracks from Soundcloud user {soundcloud_user_id}")
    print("")

    recent_tracks = get_recent_favorites(
        configs['SOUNDCLOUD_CLIENT_ID'],
        configs['SOUNDCLOUD_SECRET_ID'],
        soundcloud_user_id, num_tracks)

    for track in recent_tracks:
        print(f"{track.name}")
        if track_already_archived(configs['DOPECHEDDAR_DB'], track.track_id):
            print("-->Track already posted & archived")
            print("")
        else:
            print("-->Unique track identified. Posting to Tumblr now.")
            postTrackToTumblr(
                configs['TUMBLR_CLIENT_KEY'],
                configs['TUMBLR_CLIENT_SECRET'],
                configs['TUMBLR_RESOURCE_OWNER_KEY'],
                configs['TUMBLR_RESOURCE_OWNER_SECRET'],
                configs['TUMBLR_POST_URL'],
                track)
            print("-->Archiving in database now.")
            archive_track(configs['DOPECHEDDAR_DB'], track)
            print("-->Track was archived successfully")
            print("")

    print("-----TURNING DOWN-----")
    print("")

if __name__ == "__main__":
    main()
