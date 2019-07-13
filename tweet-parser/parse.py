from twython import Twython
import pickle
import json
from kafka import KafkaProducer
import config
from datetime import datetime
import sys

if len(sys.argv) != 2:
    print("Missing second parameter -- Hashtag")
    exit(1)

credentials     = pickle.load(open('credentials.pkl', 'rb'))

APP_KEY         = credentials['APP_KEY']
ACCESS_TOKEN    = credentials['ACCESS_TOKEN']

HASHTAG         = sys.argv[1]

print("Processing data for hashtag: " + HASHTAG)

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

print("App key: " + APP_KEY + "; Access Token: " + ACCESS_TOKEN)

try:
    # Look up the last processed Tweet ID. If it doesn't exist, we'll write it afterwards
    last_process_info_file = open('last_process_info.pkl', 'rb+')

    last_process_info = pickle.load(last_process_info_file)

    print("Fetched info!")
    # print(last_process_info)
    
    last_process_info_file.close()
except (EOFError, FileNotFoundError) as e:
    last_process_info = {}
    
if HASHTAG not in last_process_info:
    print("Creating new info")
    last_process_info[HASHTAG] = {
            'tweet_id': None,
            'timestamp': None 
        }
    
print("Fetching search results ....")



search_results = twitter.search(
    q=HASHTAG,
    lang='en', 
    # result_type='popular', 
    tweet_mode='extended',
    count=config.TWEETER_NUM_TWEETS_TO_FETCH, 
    since_id=last_process_info[HASHTAG]['tweet_id']
)

print("Search results fetched ...")
print("Sending them to Kafka ...")

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for tweet in search_results['statuses']:
    print(tweet)
    producer.send('raw_tweets', tweet)

    last_process_info[HASHTAG]['tweet_id'] = tweet['id']
    last_process_info[HASHTAG]['timestamp'] = datetime.now().timestamp()

    # print(last_process_info)
    
last_process_info_file = open('last_process_info.pkl', 'wb+')

pickle.dump(last_process_info, last_process_info_file)

last_process_info_file.close()

print("All tweets sent to Kafka ... Exiting now ...")

exit(0)

    
