import tweepy
import requests
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

### CREDENTIALS ARE PERSONAL AND CONFIDENTIAL
### TWITTER MAY BLOCK ACCESS IF FIND ANY SUSPECIOUS ACTIVITY
api_key = config['Twitter']['api_key']
api_key_secret = config['Twitter']['api_key_secret']
access_token = config['Twitter']['access_token']
access_token_secret = config['Twitter']['access_token_secret']
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHYvZgEAAAAAI1R0UNQlJn7y1t9YrSa5LLtfYlc%3Dq7Zhmxr5VQCVKxR64DpnZ0aXHPnUuAq73m6we66FtVcpZTYU88"

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
    
api = tweepy.API(auth)
def get_tweets(querry):
    ### get only 2000 tweets
    tweets  = tweepy.Cursor(api.search_tweets, q = querry, count = 100, tweet_mode='extended').items(200)
    
    aber_data = []
    for tweet in tweets:
        aber_data.append([tweet.id_str,
                        tweet.author,
                        tweet.user.id_str,
                        tweet.user.screen_name,
                        tweet.user.verified,
                        tweet.user.followers_count,
                        tweet.user.time_zone,
                        tweet.user.geo_enabled,
                        tweet.full_text,
                        tweet.created_at,
                        tweet.favorite_count,
                        tweet.geo,
                        tweet.user.location,
                        tweet.coordinates, 
                        tweet.place, 
                        tweet.lang])
    df = pd.DataFrame(aber_data, columns = ["tweet_id", "tweet_author", "user_id", "user_screen_name", "verified", "followers_count", "user_timezone", "geo_enabled", "tweet", "time", "likes_count", "geo", "userlocation", "cords", "place", "lang"])
    df.to_csv("twitter_"+str(querry)+"data.csv")
    return df

