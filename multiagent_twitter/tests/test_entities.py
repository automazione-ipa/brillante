import unittest
from datetime import datetime, timedelta
import uuid
from logic.entities import Tweet


class TestTweetEntity(unittest.TestCase):
    """
    Unit test per verificare la corretta creazione e integrità dell'oggetto Tweet.
    """

    def test_tweet_creation_default(self):
        """Testa la creazione di un tweet con valori di default."""
        tweet = Tweet(testo="Questo è un test tweet.")

        self.assertIsInstance(tweet.uid, str, "L'UID deve essere una stringa.")
        self.assertTrue(uuid.UUID(tweet.uid),
                        "L'UID deve essere un UUID valido.")
        self.assertEqual(tweet.testo, "Questo è un test tweet.",
                         "Il testo del tweet non corrisponde.")
        self.assertIsInstance(tweet.created_at, datetime,
                              "created_at deve essere un oggetto datetime.")
        self.assertLessEqual(tweet.created_at, datetime.utcnow(),
                             "created_at non può essere nel futuro.")

    def test_tweet_creation_with_custom_values(self):
        """Testa la creazione di un tweet con valori personalizzati."""
        custom_uid = str(uuid.uuid4())
        custom_time = datetime.utcnow() - timedelta(days=1)
        tweet = Tweet(uid=custom_uid, testo="Test con valori personalizzati.",
                      created_at=custom_time)

        self.assertEqual(tweet.uid, custom_uid,
                         "L'UID personalizzato non è stato assegnato correttamente.")
        self.assertEqual(tweet.testo, "Test con valori personalizzati.",
                         "Il testo personalizzato non corrisponde.")
        self.assertEqual(tweet.created_at, custom_time,
                         "La data di creazione personalizzata non corrisponde.")

    def test_tweet_uid_uniqueness(self):
        """Verifica che due tweet abbiano UID diversi per impostazione predefinita."""
        tweet1 = Tweet(testo="Tweet 1")
        tweet2 = Tweet(testo="Tweet 2")

        self.assertNotEqual(tweet1.uid, tweet2.uid,
                            "Ogni tweet deve avere un UID univoco.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
