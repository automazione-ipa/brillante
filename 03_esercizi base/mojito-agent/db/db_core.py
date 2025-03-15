from pymongo import MongoClient


class DBCore:
    def __init__(
        self,
        connection_string="mongodb://localhost:27017/",
        db_name="cocktails_db"
    ):
        """Inizializza la connessione a MongoDB."""
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        # Collezione per i cocktail
        self.cocktails_collection = self.db["cocktails"]
        # Collezione per gli ingredienti
        self.ingredients_collection = self.db["ingredients"]

    def save_ingredient(self, ingredient_name: str, ingredient_details: dict):
        """
        Salva un ingrediente nel database MongoDB.
        :param ingredient_name: nome dell'ingrediente
        :param ingredient_details: dettagli aggiuntivi sull'ingrediente (es. tipo, marca, ecc.)
        :return: l'ID generato da MongoDB per il documento inserito
        """
        document = {
            "name": ingredient_name.lower(),
            **ingredient_details
        }
        result = self.ingredients_collection.insert_one(document)
        return result.inserted_id

    def save_cocktail_recipe(self, cocktail_name: str, ingredients: list, preparation: str):
        """
        Salva la ricetta di un cocktail nel database MongoDB.
        :param cocktail_name: nome del cocktail
        :param ingredients: lista di ingredienti, ognuno referenziato tramite l'ID dell'ingrediente
        :param preparation: descrizione della preparazione
        :return: l'ID generato da MongoDB per il documento inserito
        """
        document = {
            "cocktail_name": cocktail_name.lower(),
            "ingredients": ingredients,  # Lista di riferimenti agli ID degli ingredienti
            "preparation": preparation
        }
        result = self.cocktails_collection.insert_one(document)
        return result.inserted_id

    def get_cocktail_recipe(self, cocktail_name: str):
        """
        Cerca e restituisce la ricetta per il cocktail dal database.
        :param cocktail_name: nome del cocktail da cercare
        :return: la ricetta se trovata, altrimenti None
        """
        document = self.cocktails_collection.find_one({"cocktail_name": cocktail_name.lower()})
        if document:
            # Recupera gli ingredienti dal database per ogni ID
            ingredients = []
            for ingredient_id in document["ingredients"]:
                ingredient = self.ingredients_collection.find_one({"_id": ingredient_id})
                if ingredient:
                    ingredients.append(ingredient["name"])
            document["ingredients"] = ingredients
            return document
        return None

    def get_ingredient_by_name(self, ingredient_name: str):
        """
        Cerca un ingrediente nel database per nome.
        :param ingredient_name: nome dell'ingrediente da cercare
        :return: il documento dell'ingrediente, altrimenti None
        """
        return self.ingredients_collection.find_one({"name": ingredient_name.lower()})

    def close(self):
        """Chiude la connessione a MongoDB."""
        self.client.close()

    # Gestione del contesto (with)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
