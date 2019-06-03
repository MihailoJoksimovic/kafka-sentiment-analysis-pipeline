# Loads data from Kafka, runs Sentiment analysis and stores data back to Kafka

from afinn import Afinn
import json
from kafka import KafkaConsumer
from kafka import KafkaProducer
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from elasticsearch import Elasticsearch
import pandas as pd
from nltk.tokenize import TweetTokenizer
import time
import re

nrc_lexicon = pd.read_csv('./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', header = None, sep="\t", names=["word", "emotion", "yes_or_no"])
nrc_lexicon.set_index(['word'], inplace=True)

def get_emotions_in_sentence(sentence):
    """Takes a sentence as an input, and returns a dictionary of emotions and number of
    occurences for them.
    
    For example, given: "I am so joyful and happy that I'm here" on input, returns:

        {'joy': 2, 'positive': 2, 'trust': 2, 'anticipation': 1}
    
    on output.
    """
    tknzr = TweetTokenizer()
    
    tokens = tknzr.tokenize(sentence)
    
    emotions = {}
    
    for word in tokens:
        # Replace hashtags with pure words (i.e. "#positive" becomes "positive")
        if re.match("^#\S+", word):
            word = re.sub("^#", "", word)
        
        try:
            _emotions = nrc_lexicon.loc[word]
            
            _emotions = _emotions[_emotions['yes_or_no'] == 1]
            
            if _emotions[_emotions['yes_or_no'] == 1].empty:
                pass
            
            for _emotion in _emotions[_emotions['yes_or_no'] == 1]['emotion']:
                if _emotion not in emotions:
                    emotions[_emotion] = 0

                emotions[_emotion] += 1 
        except:
            pass
        
    return emotions

consumer = KafkaConsumer('raw_tweets', 
                         auto_offset_reset='smallest',
                         group_id='sentiment_analysers', 
                         value_deserializer=lambda v: json.loads(v)
)

producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

afinn = Afinn()

es = Elasticsearch()

for msg in consumer:
    print("\n\n\nProcessing new message: ")
    print(msg.value['full_text'])

    msg.value['afinn_score'] = afinn.score(msg.value['full_text'])
    msg.value['emotions'] = get_emotions_in_sentence(msg.value['full_text'])
    
    print("\nAFINN score: ")
    print(msg.value['afinn_score'])
    
    print("\nEmotions: ")
    print(msg.value['emotions'])

    producer.send('processed_tweets', msg.value)
    
    es.index(index="processed_tweets", body=msg.value, id=msg.value['id'])

