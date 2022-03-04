import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import emoji
import advertools as adv
import re
import string
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import collections

import warnings
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')


def read_data():
	data = pd.read_csv("/home/purna/PURNA_OFFICE/Task-37 Twitter_sentement_analysis/vitoriassecret_data/2000_rows_victoriadata_recent.csv")
	data1= data.copy()
	return data1

def clean(data1):
	data1 = data1.rename(columns = {"Unnamed: 0":"index"})
	data1 = data1.drop('user_timezone',axis = 1) # 0 values
	data1 = data1.drop('user_id', axis = 1)
	data1 = data1.drop('tweet_id', axis = 1)
	data1 = data1.drop('tweet_encoded', axis  =1) # same as tweet column
	data1 = data1.drop('geo_enabled', axis = 1) # still had location, when set to False
	data1 = data1.drop('geo', axis = 1) # only 3rows had information
	data1 = data1.drop('cords', axis  =1) # geo and cords columns are same
	data1 = data1.drop('place', axis  =1) # only 10 fileds available
	return data1

def remove_URL(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", sample)

def word_frequency(data1):
	all_tweets = []
	for tweet in data1['tweet']:
		cleaned_tweet = remove_URL(tweet).replace("#victoriassecret","").replace("#","").replace("\'","").lower()
		all_tweets.append(cleaned_tweet)

	tokened_text = [text.split(" ") for text in all_tweets]
	tokened_text = [token.strip(string.punctuation) for token_text in tokened_text for token in token_text if token != '']

	stopwords = set(STOPWORDS)

	filtered_text = [word for word in tokened_text if word not in stopwords]
	counted_text = collections.Counter(filtered_text)
	final = sorted(counted_text.items(), key=lambda item: item[1],reverse= True)[:10]
	word = [i[0] for i in final]
	freq = [i[1] for i in final]
	sampledf = pd.DataFrame({"words" :word, "frequency":freq})
	return sampledf

def getemoji(data1):
	all_tweets = []
	for tweet in data1['tweet']:
		cleaned_tweet = remove_URL(tweet).replace("#victoriassecret","").replace("#","").replace("\'","").lower()
		all_tweets.append(cleaned_tweet)
	emoji_summary = adv.extract_emoji(all_tweets)
	return emoji_summary['top_emoji']

def preprocess(data1):
	full_cleaned_tweets = []
	for tweet in data1['tweet']:
		lower_tweet = tweet.lower() #lower text
		no_url_tweet = remove_URL(lower_tweet) # remove urls
		no_mentions_tweet = re.sub("@[A-Za-z0-9_]+","", no_url_tweet) #remove mentions
		no_hashtag_tweet = re.sub("#[A-Za-z0-9_]+","", no_mentions_tweet) #remove hashtags
		no_emoji_tweet = re.sub(r"[^a-zA-Z0-9]", " ",no_hashtag_tweet) #just alphanumeric
		striped_tweet = " ".join(no_emoji_tweet.split()) #stipped longer white space
		full_cleaned_tweets.append(striped_tweet)
	return full_cleaned_tweets