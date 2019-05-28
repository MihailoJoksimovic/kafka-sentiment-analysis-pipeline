# Script obtains access token for Twitter

import pickle
from twython import Twython

credentials_fh  = open('credentials.pkl', 'rb')

credentials     = pickle.load(credentials_fh)

credentials_fh.close()

APP_KEY         = credentials['APP_KEY']
APP_SECRET      = credentials['APP_SECRET']

twitter         = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN    = twitter.obtain_access_token()

print("Access token is: " + ACCESS_TOKEN)

credentials['ACCESS_TOKEN'] = ACCESS_TOKEN

credentials_fh_writer = open('credentials.pkl', 'wb')

pickle.dump(credentials, credentials_fh_writer)

credentials_fh_writer.close()