
# Twitter Bots/twitter_config.py
import tweepy
import logging
import os
from os import environ



logger = logging.getLogger()

def create_api():

    twitter_consumer_key = environ["TWITTER_CONSUMER_KEY"]
    twitter_consumer_secret = environ["TWITTER_CONSUMER_SECRET"]
    twitter_access_token = environ["TWITTER_ACCESS_TOKEN"]
    twitter_access_token_secret = environ["TWITTER_ACCESS_TOKEN_SECRET"]
    
    
    
    
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

