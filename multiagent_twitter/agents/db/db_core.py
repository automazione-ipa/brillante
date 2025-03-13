from pymongo import MongoClient
from logic.entities import Tweet


class DBCore:
    def __init__(
            self,
            connection_string="mongodb://localhost:27017/",
            db_name="twitter_db"
    ):
        """Inizializza la connessione a MongoDB."""
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db["tweets"]

    def save_tweet(self, tweet: Tweet):
        """
        Salva il tweet nel database MongoDB.
        :param tweet: istanza di Tweet (Pydantic model)
        :return: l'ID generato da MongoDB per il documento inserito
        """
        tweet_dict = tweet.model_dump()
        result = self.collection.insert_one(tweet_dict)
        return result.inserted_id

    def close(self):
        """Chiude la connessione a MongoDB."""
        self.client.close()

    # Gestione automatica della chiusura; contesto:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
