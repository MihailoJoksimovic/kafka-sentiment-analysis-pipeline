from twython import Twython
import pickle
import json
from kafka import KafkaProducer

credentials     = pickle.load(open('credentials.pkl', 'rb'))

APP_KEY         = credentials['APP_KEY']
ACCESS_TOKEN    = credentials['ACCESS_TOKEN']

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

print("App key: " + APP_KEY + "; Access Token: " + ACCESS_TOKEN)
print("Fetching search results ....")

search_results = twitter.search(q='#gameofthrones', lang='en', result_type='popular', count=10)

print("Search results fetched ...")
print("Sending them to Kafka ...")

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for tweet in search_results['statuses']:
    print(tweet)
    producer.send('__gameofthrones', tweet)
    
print("All tweets sent to Kafka ... Exiting now ...")

    
