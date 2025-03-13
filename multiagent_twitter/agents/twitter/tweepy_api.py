from typing import Optional, List, Union

import tweepy
from dotenv import load_dotenv

load_dotenv()


class TwitterAPIWrapper:
    def __init__(
            self,
            consumer_key: str, consumer_secret: str,
            access_token: str, access_token_secret: str,
    ):
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def publish_tweet(
            self,
            text: str,
            place_id: Optional[str] = None,
            media_ids: Optional[List[Union[int, str]]] = None,
            media_tagged_user_ids: Optional[List[Union[int, str]]] = None,
    ):
        """
        Publishes a tweet.

        :param text: The tweet content
        :param place_id: (Optional) The ID of the place of twitter
        :param media_ids: (Optional) List of media IDs to attach
        :param media_tagged_user_ids: (Optional) List of media tagged user IDs to attach
        """
        response = self.client.create_tweet(
            text=text,
            place_id=place_id,
            media_ids=media_ids,
            media_tagged_user_ids=media_tagged_user_ids,
        )

        return response
