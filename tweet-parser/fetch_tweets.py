from twython import Twython
import pickle
import json
import sys
import os
import csv
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import time
from elasticsearch import Elasticsearch

# if len(sys.argv) != 2:
#     print("Missing second parameter -- Hashtag")
#     exit(1)

credentials = pickle.load(open('credentials.pkl', 'rb'))

APP_KEY = credentials['APP_KEY']
ACCESS_TOKEN = credentials['ACCESS_TOKEN']

# HASHTAG = sys.argv[1]
HASHTAG = "#sad"

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

es = Elasticsearch()

def do_the_fetch():
    try:
        with open('last_fetched_tweet.pkl') as f:
            tweet_id = f.readline()
    except:
        tweet_id = None

    search_results = twitter.search(
        q=HASHTAG,
        lang='en',
        tweet_mode='extended',
        count=1000,
        max_id=tweet_id
    )

    last_tweet_id = None

    # for status in search_results.statuses:

    for status in search_results['statuses']:
        print(status['full_text'])
        print("\n\n\n")

        try:
            es.index(index="raw_tweets", body=status, id=status['id'])
        except RequestError:
            pass

        last_tweet_id = status['id']

    with open('last_fetched_tweet.pkl', "w+") as f:
        f.write(str(last_tweet_id))


for i in range(5):
    do_the_fetch()
