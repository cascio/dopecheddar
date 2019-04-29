"""Twitter API related functionality"""

from track_data import get_random_unposted_twitter_track, posted_to_twitter
from os import environ
from urllib.parse import quote_plus
import oauth2

def set_environment():
    """Retrieves Twitter configurations from enviroment variables"""
    required_env_vars = {
        'DOPECHEDDAR_DB': None,
        'TWITTER_CONSUMER_API_KEY': None,
        'TWITTER_CONSUMER_API_SECRET_KEY': None,
        'TWITTER_ACCESS_TOKEN': None,
        'TWITTER_ACCESS_SECRET': None,
    }

    for var in required_env_vars:
        if var in environ:
            required_env_vars[var] = environ[var]
        else:
            print(f"Environment Variable: {var} not set. Set the env var  and try again.")
            exit()
    return required_env_vars

def main():
    """Tweets a random track from the dopecheddar database"""
    configs = set_environment()
    random_track = get_random_unposted_twitter_track(configs['DOPECHEDDAR_DB'])
    consumer = oauth2.Consumer(key=configs['TWITTER_CONSUMER_API_KEY'], secret=configs['TWITTER_CONSUMER_API_SECRET_KEY'])
    token = oauth2.Token(key=configs['TWITTER_ACCESS_TOKEN'], secret=configs['TWITTER_ACCESS_SECRET'])
    client = oauth2.Client(consumer, token)
    payload = quote_plus(random_track.name + '\n\n' + '#dopecheddar #electronicmusic' + '\n' + random_track.url)
    url = "https://api.twitter.com/1.1/statuses/update.json?status=" + payload
    successfulTweet = False
    while successfulTweet == False:
        resp, content = client.request(url, method="POST", body="", headers=None)
        if resp.status == 200:
            print("Tweet Was Successful", end='\n\n')
            posted_to_twitter(configs['DOPECHEDDAR_DB'], random_track)
            successfulTweet = True
        else:
            print('Tweet Was NOT Successful', end='\n\n')
            print(f'Response:\n{resp}', end='\n\n')
            print(f'Content:\n{content}', end='\n\n')
            break

if __name__ == "__main__":
    main()
