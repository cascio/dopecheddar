from soundcloud_tools import get_recent_favorites
from track_data import archive_track, track_already_archived

# set soundcloud_user_id to target and num_tracks to retreive
soundcloud_user_id = '50163285' # dopecheddar's account id ;)
num_tracks = 2

recent_tracks = get_recent_favorites(soundcloud_user_id, num_tracks)

for track in recent_tracks:  
    if track_already_archived(track.track_id):
        print("Track Is Already In Database")
        pass
    else:
        print("Track Is Not Yet Saved To Database......Saving Now")
        # archive_track(track)
        print("Track Archived Successfully")
