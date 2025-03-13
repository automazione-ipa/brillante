import unittest
from datetime import datetime
import logging
from logic.entities import Tweet
from agents.db.db_core import DBCore

# Configura il logging
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestDBCore(unittest.TestCase):
    """
    Classe di test per la gestione del database tramite DBCore.
    """

    def setUp(self) -> None:
        """
        Imposta una connessione al database di test e pulisce la collezione.
        """
        logger.info("Setting up test DB connection")
        self.db_core = DBCore(
            connection_string="mongodb://localhost:27017/",
            db_name="twitter_db_test"
        )
        self.db_core.collection.delete_many({})
        logger.info("Test collection cleaned")

    def tearDown(self):
        """
        Pulisce la collezione dopo ogni test e chiude la connessione al database.
        """
        logger.info("Cleaning up test collection and closing connection")
        self.db_core.collection.delete_many({})
        self.db_core.close()

    def test_save_tweet(self):
        """
        Test per verificare il salvataggio di un tweet nel database.

        1. Crea un tweet di test.
        2. Salva il tweet nel database.
        3. Recupera il tweet dal database: verifica corretto inserimento.
        """
        logger.info("Starting test_save_tweet")
        tweet = Tweet(
            testo="Questo è un tweet di test.", created_at=datetime.utcnow()
        )
        inserted_id = self.db_core.save_tweet(tweet)
        self.assertIsNotNone(
            inserted_id,
            "Il tweet non è stato salvato correttamente."
        )
        logger.info(f"Tweet inserted with id: {inserted_id}")

        saved_tweet = self.db_core.collection.find_one({"uid": tweet.uid})
        self.assertIsNotNone(
            saved_tweet,
            "Nessun documento trovato nel database per l'UID specificato."
        )
        self.assertEqual(
            saved_tweet.get("testo"),
            tweet.testo,
            "Il testo del tweet salvato non corrisponde a quello atteso."
        )
        logger.info("Test completed successfully")


if __name__ == '__main__':
    unittest.main(verbosity=2)
