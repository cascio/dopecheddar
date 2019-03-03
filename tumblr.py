from os import environ
from requests_oauthlib import OAuth1Session
import time

def startOauth(client_key, client_secret, resource_owner_key, resource_owner_secret):
    oauth = OAuth1Session(
        client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        signature_type='auth_header'
    )
    return oauth

def createTumblrPayload(track):
    track_url = track.url
    track_name = track.name
    dopecheddarSoundcloudURL = 'www.soundcloud/dopecheddar'
    postText = 'Follow DOPECHEDDAR on Soundcloud!'
    postCaption = '<a href="%s">%s</a><br></br><br></br><br></br><br></br><a href="%s">%s</a>' % (track_url, track_name, dopecheddarSoundcloudURL, postText)
    payload = {'type': 'audio', 'caption': postCaption, 'external_url': track_url, 'tags': track.tag_list}
    return payload

def postTrackToTumblr(client_key, client_secret, resource_owner_key, resource_owner_secret, post_url, track):
    oauth = startOauth(client_key, client_secret, resource_owner_key, resource_owner_secret)
    payload = createTumblrPayload(track)
    successfulPost = False

    # The code below needs to be revisited because it is probably not the right solution to the problem
    # where Tumblr randomly throws a 400 request status code even if you'rs below the rate limit.
    # When I previously research this problem online, simply waiting and retrying was a solution that worked...
    while successfulPost == False:
        req = oauth.post(post_url, data=payload)
        if req.status_code == 400:
            print(f"-->{req.content}")
            print("-->Posting to Tumblr was not successful")
            print("-->Waiting a couplah seconds")
            time.sleep(3)
            print("-->Trying to post to Tumblr again")
        elif req.status_code == 401:
            print(f"-->{req.content}")
            print("-->Woops...401 Error")
            break
        else:
            print("-->Track was successfully posted to Tumblr:")
            print(f"-->{req.content}")
            successfulPost = True