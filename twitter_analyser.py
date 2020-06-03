from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import Twitter_Credentials
import pandas as  pd
import numpy as np
import matplotlib.pyplot as plt


###Twitter Clients ###

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets




### Twitter Authenticator ###
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(Twitter_Credentials.CONSUMER_KEY, Twitter_Credentials.CONSUMER_SECRET_KEY)
        auth.set_access_token(Twitter_Credentials.ACCESS_KEY,Twitter_Credentials.ACCESS_SECRET_KEY)
        return auth

###Twitter Streamer###

##Class for streaming and processing live tweets###


class TwitterStreamer():
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth=self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list )


        ###Twitter Stream Listener###

class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    
    def on_error(self, status):
        if status == 420:
            return False
        print(status)

class TweetAnalyzer():
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets ], columns = ['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        #df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])


        return df

    





if __name__ == '__main__':
   twitter_client = TwitterClient()
   tweet_analyzer = TweetAnalyzer()
   api = twitter_client.get_twitter_client_api()
   tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)
   
   
   df = tweet_analyzer.tweets_to_data_frame(tweets)
   
   #print(df.head(10))
   #print(dir(tweets[0]))
   #print(tweets[0].retweet_count)

   #average
   print(np.mean(df['len']))

   #max likes
   print(np.max(df['likes']))
   
   #max retweets
   print(np.max(df['retweets']))

   time_likes = pd.Series(df['likes'].values, index = df['date'])
   time_likes.plot(figsize=(16,4), label="likes", legend=True)
   
    
   time_retweets = pd.Series(df['retweets'].values, index = df['date'])
   time_retweets.plot(figsize=(16,4), label="retweets", legend=True)
   plt.show()

   
   



    
   