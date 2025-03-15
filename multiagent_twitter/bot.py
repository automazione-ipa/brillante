import os
from dotenv import load_dotenv

from agents.db.db_core import DBCore
from agents.twitter.tweepy_api import TwitterAPIWrapper
from agents.openai_agent.chat_agent import ChatAgent

load_dotenv()


def is_tweet_ready(tweet: str) -> bool:
    """
    Placeholder. Should calculate a truthness value based on some rules.

    If rules are met, then the post is ready and we can return TRUE, otherwise returns FALSE.

    """
    return True


def create_post(topic: str):
    """
    Instantiates necessary agents and implements the createPost() procedure.
    """
    # DBCore (database-agent)
    db_core = DBCore(
        connection_string=os.getenv("DB_CONNECTION_STRING"),
        db_name=os.getenv("DB_NAME")
    )
    # TwitterAPIWrapper (twitter-agent)
    # BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    twitter = TwitterAPIWrapper(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
    # ChatAgent (openai-agent)
    chat = ChatAgent(
        api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini"
    )

    # 1. Genera il Tweet con openai
    tweet = chat.generate_tweet(
        prompt=f"Genera un tweet coinvolgente e conciso sull'argomento: {topic}"
    )
    print(f"\nTweet generato:\n{tweet}")
    # 2. Salva il Tweet su database
    tweet_id = db_core.save_tweet(tweet)
    print(f"Tweet salvato nel database con id: {tweet_id}")
    # 3. Se il Tweet è pronto, pubblica su X
    publish_confirmation = is_tweet_ready(tweet.testo)
    if publish_confirmation:
        twitter.publish_tweet(tweet.testo)
    else:
        print("Tweet non pubblicato, richiede ulteriori modifiche.")


if __name__ == "__main__":
    create_post(topic="ETHEREUM CRYPTO DAOs: caso studio su YEARN FINANCE ed $YFI")
