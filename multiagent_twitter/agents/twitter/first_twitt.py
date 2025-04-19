import os
from dotenv import load_dotenv
from agents.twitter.tweepy_api import TwitterAPIWrapper

load_dotenv()

if __name__ == "__main__":
    BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

    consumer_key: str = os.getenv("TWITTER_API_KEY")
    consumer_secret: str = os.getenv("TWITTER_API_SECRET")
    access_token: str = os.getenv("ACCESS_TOKEN")
    access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET")
    twitter = TwitterAPIWrapper(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )

    tweet_text = "Hello Twitter! This is a test of Post a post via X API v2 wrapper written in python. #TestTweet"

    twitter.publish_tweet(tweet_text)
