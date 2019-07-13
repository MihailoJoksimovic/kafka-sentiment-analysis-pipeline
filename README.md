# kafka-sentiment-analysis-pipeline

University project done for "Text Mining" subject.

Pipeline that consits of:

- Twitter parser --> script that parses tweets for a given hashtag and stores them to Kafka
- Sentiment analyser --> reads unprocessed tweets from Kafka, runs sentiment analysis (using AFINN and NRC lexicons) and stores data back to Kafka and Elastic Search
- Frontend that displays summarized data for each hashtag (i.e. how many positive/negative/neutral tweets are there for each tweet + the emotions identified using NRC lexicon)

Additionally, in "tweeter-parser" folder, there is a number of Jupyter notebooks where I attempted to run classification against each tweet. Specifically, the idea was to classify tweets into "happy" or "sad" category.

Vectorization was done using TF-IDF vectorizer, both using the Sci-kit learn one and using a manually built one.

There are also examples of classification using Porter Stemmer and WordNet Lemmatizer.

All the data is summarize under PPTX presentation which can be downloaded from:
https://drive.google.com/open?id=14ojJjZ32WzpozU7g7IWzdeQ4LeIDKYsy

