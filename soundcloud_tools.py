from track_data import SoundcloudTrack
import soundcloud

# retreive the latest "n" tracks favorited by a "soundcloud_user_id"
# returns a soundcloud.resource.Resource object with requested track info
def get_recent_favorites(client_id, client_secret, soundcloud_user_id, n):
    path = '/users/%s/favorites' % str(soundcloud_user_id)
    limit = int(n)
    # initialize soundcloud API client
    soundcloud_client = soundcloud.Client(client_id=client_id, client_secret=client_secret)
    try:
        recent_tracks = soundcloud_client.get(path, limit=limit)
        converted_tracks = convert_to_SoundcloudTrack(recent_tracks)
        return converted_tracks
    except Exception as error:
        print('Error: %s, Status Code: %d' % (error.message, error.response.status_code))

# convert tracks received from soundcloud to custom SoundcloudTrack class
# returns a list of SoundcloudTracks
def convert_to_SoundcloudTrack(tracks_from_soundcloud):
    soundcloud_tracks = []
    for track in tracks_from_soundcloud:
        soundcloud_track = SoundcloudTrack(track.title, track.id, track.permalink_url, track.genre, track.label_name, track.tag_list)
        soundcloud_tracks.append(soundcloud_track)
    return soundcloud_tracks