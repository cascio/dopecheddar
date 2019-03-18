'''Soundcloud API related functionality'''

import soundcloud
from track_data import SoundcloudTrack

def get_recent_favorites(client_id, client_secret, soundcloud_user_id, num_tracks):
    '''Retreives the latest tracks favorited by a soundcloud user by id.
    Returns a soundcloud.resource.Resource object holding the tracks'''
    path = '/users/%s/favorites' % str(soundcloud_user_id)
    limit = int(num_tracks)
    # initialize soundcloud API client
    soundcloud_client = soundcloud.Client(client_id=client_id, client_secret=client_secret)
    try:
        recent_tracks = soundcloud_client.get(path, limit=limit)
        converted_tracks = convert_to_soundcloud_track(recent_tracks)
        return converted_tracks
    except Exception as error:
        print('Error: %s, Status Code: %d' % (error.message, error.response.status_code))

def convert_to_soundcloud_track(tracks_from_soundcloud):
    '''Converts tracks received from the soundcloud api to a custom
    SoundcloudTrack class. Returns a list of SoundcloudTracks'''
    soundcloud_tracks = []
    for track in tracks_from_soundcloud:
        soundcloud_track = SoundcloudTrack(
            track.title,
            track.id,
            track.permalink_url,
            track.genre,
            track.label_name,
            track.tag_list)
        soundcloud_tracks.append(soundcloud_track)
    return soundcloud_tracks
