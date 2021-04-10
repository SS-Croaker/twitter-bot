# https://realpython.com/twitter-bot-python-tweepy/

import tweepy
from time import sleep 
import logging
from twitter_config import create_api
import random
# Authenticate to Twitter
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token,access_token_secret)

#api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

#try:
#    api.verify_credentials()
#    print("Authentication OK")
#except:
#    print("Error during authentication")

api = create_api()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#def retrieve_last_retweet_id(file_name):
#    f_read = open(file_name,'r')
#    last_retweet_id = int(f_read.read().strip())
#    f_read.close()
#    return last_retweet_id        

#this function is to store the tweet ids that the bot has retweeted

def store_last_retweet_id(last_retweet_id,last_retweet_username,file_name):
    f_write = open(file_name,'a')
    f_write.write('\n')
    f_write.write(str(last_retweet_id) + ' - ' + str(last_retweet_username))
    f_write.close()
    return

file_name_retweet = 'Last_Retweet_Tweet_ID.txt' 

#read about SteamListener Class of tweepy

class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        
        logger.info(f"Processing tweet id {tweet.id}")
        
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        
        # if not tweet.retweeted checks if my account has retweeted the tweet or not
        # if 'RT @' not in tweet.text check is the tweet is NOT a retweet
        #favourites_count = tweet.favourites_count
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            
            try:
                sleep_time = random.randrange(600,1200,60)
                print(sleep_time)
                                               
                tweet.retweet()
                print('-----\n')
                print(tweet.id)
                last_retweet_id = tweet.id
                                
                print('\nTweet by: @' + tweet.user.screen_name)
                last_retweet_username = tweet.user.screen_name
                
                store_last_retweet_id(last_retweet_id,last_retweet_username,file_name_retweet)
                print('Retweeted the tweet')
                sleep(sleep_time)
                
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    
    def on_error(self, status):
        logger.error(status)

       
        
def main(keywords):
    api = create_api()
    tweets_listener = RetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])
    

if __name__ == "__main__":
    main(["marketingtwitter"])
