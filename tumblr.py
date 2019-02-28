from os import environ
from requests_oauthlib import OAuth1Session

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
    while successfulPost == False:
        req = oauth.post(post_url, data=payload)
        if req.content[18:24] == "400":
            print(r.content)
            print("-->Posting to Tumblr was not successful")
            print("-->Waiting a couplah seconds")
            time.sleep(3)
            print("-->Trying again")
        else:
            print(req.content)
            print("-->Posting to Tumblr was successful")
            print(2 * "")
            successfulPost = True