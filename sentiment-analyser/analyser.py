# Loads data from Kafka, runs Sentiment analysis and stores data back to Kafka

from afinn import Afinn
import json
from kafka import KafkaConsumer
from kafka import KafkaProducer
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from elasticsearch import Elasticsearch

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
    
    print("\nAFINN score: ")
    print(msg.value['afinn_score'])

    producer.send('processed_tweets', msg.value)
    
    es.index(index="processed_tweets", body=msg.value, id=msg.value['id'])

