from os import environ
from requests_oauthlib import OAuth1Session
import time

def startOauth(client_key, client_secret, resource_owner_key, resource_owner_secret):
    """Creates Oauth1 Session with keys from enivornment variables"""
    oauth = OAuth1Session(
        client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        signature_type='auth_header'
    )
    return oauth

def createTumblrPayload(track):
    """Assembles the expected Tumblr payload for post creation"""
    track_url = track.url
    track_name = track.name
    dopecheddarSoundcloudURL = 'www.soundcloud/dopecheddar'
    postText = 'Follow DOPECHEDDAR on Soundcloud!'
    postCaption = '<a href="%s">%s</a><br></br><br></br><br></br><br></br><a href="%s">%s</a>' % (track_url, track_name, dopecheddarSoundcloudURL, postText)
    payload = {'type': 'audio', 'caption': postCaption, 'external_url': track_url, 'tags': track.tag_list}
    return payload

def postTrackToTumblr(client_key, client_secret, resource_owner_key, resource_owner_secret, post_url, track):
    """Executes the post request to Tumblr. 401 errors are skipped, 400 errors are attempted three times before skipping"""
    oauth = startOauth(client_key, client_secret, resource_owner_key, resource_owner_secret)
    payload = createTumblrPayload(track)
    successfulPost = False
    tries = 0
    while successfulPost == False:
        req = oauth.post(post_url, data=payload)
        tries += 1
        if req.status_code == 400:
            print(f"-->{req.content}")
            print("-->Posting to Tumblr was not successful")
            if tries < 4:
                print("-->Waiting a couplah seconds")
                time.sleep(3)
                print("-->Trying to post to Tumblr again")
            else:
                return False
        elif req.status_code == 401:
            print(f"-->{req.content}")
            print("-->Woops...401 Error")
            return False
        else:
            print("-->Track was successfully posted to Tumblr:")
            print(f"-->{req.content}")
            successfulPost = True
    return True