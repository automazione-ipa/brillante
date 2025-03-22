import os
from typing import List

from dotenv import load_dotenv
import json

from db.db_core import DBCore
from openai_agent.chat_agent import ChatAgent
from logic.entities import CocktailRecipe

load_dotenv()


class CocktailAgent:
    def __init__(self, api_key, connection_string, db_name):
        self.db_core = DBCore(connection_string, db_name)
        self.chat_agent = ChatAgent(api_key, model="gpt-4o-mini")

    @staticmethod
    def parse_gpt_message_to_cocktail_recipe(
            str_gpt_res: str) -> CocktailRecipe:
        try:
            recipe_data = json.loads(str_gpt_res)
            return CocktailRecipe(**recipe_data)
        except json.JSONDecodeError:
            print("\nErrore: La risposta generata non è un JSON valido.")
            print("Risposta ricevuta:")
            print(str_gpt_res)
        except Exception as e:
            print(f"\nErrore durante l'elaborazione dei dati: {e}")
            print("Risposta ricevuta:")
            print(str_gpt_res)

    def save_ingredients(self, recipe: CocktailRecipe) -> List[str]:
        """Saves each ingredient into the database"""
        print(f"Cocktail Name: {recipe.cocktail_name}")
        print("Ingredients:")

        ingredients = []
        for ingredient in recipe.ingredients:
            ingredient_id = self.db_core.save_ingredient(
                ingredient.name, ingredient.quantity, ingredient.type
            )
            ingredients.append(ingredient_id)
            print(f"Ingrediente salvato nel database con id: {ingredient_id}")

        return ingredients

    def save_recipe(self, recipe: CocktailRecipe, ingredients: List[str]):
        """Saves a cocktail into the database."""
        return self.db_core.save_cocktail_recipe(
            cocktail_name=recipe.cocktail_name,
            ingredients=ingredients,
            preparation=recipe.preparation
        )

    def pipeline_structured_output(self):
        """Retrieves a receipt from GPT and adds it to the database."""

        while True:
            print("\n=== Ricerca o generazione ricetta per cocktail ===")

            cocktail_name = input(
                "Inserisci il nome di un cocktail (es. mojito, margarita, negroni) o 'exit' per uscire: ").strip().lower()
            if cocktail_name == "exit":
                print("Arrivederci!")
                break

            recipe = self.db_core.get_cocktail_recipe(cocktail_name)
            if recipe:
                print(
                    f"\nRicetta trovata nel database per {cocktail_name.capitalize()}:\n{recipe}")
            else:
                print(
                    f"\nNessuna ricetta trovata per {cocktail_name.capitalize()} nel database.")

                prompt_json = (
                    f"Genera una ricetta dettagliata per il cocktail chiamato '{cocktail_name.capitalize()}' nel formato JSON. "
                    "La risposta deve includere i seguenti campi:\n\n"
                    "{\n"
                    "  'cocktail_name': '<NomeCocktail>',\n"
                    "  'ingredients': [\n"
                    "    {'name': '<NomeIngrediente1>', 'quantity': '<quantità1>', 'type': '<tipo1>'},\n"
                    "    {'name': '<NomeIngrediente2>', 'quantity': '<quantità2>', 'type': '<tipo2>'},\n"
                    "    ...\n"
                    "  ],\n"
                    "  'preparation': '<Descrizione della preparazione>'\n"
                    "}\n\n"
                    "Assicurati che il formato JSON sia valido, con tutte le informazioni necessarie."
                )

                gpt_response = self.chat_agent.generate_receipt(
                    user_prompt=prompt_json)
                str_gpt_res = gpt_response.testo

                if str_gpt_res:
                    str_gpt_res_cleaned = str_gpt_res.strip(
                    ).strip("```").replace("json", "").strip()
                    print(
                        f"\nRicetta generata da GPT per {cocktail_name.capitalize()}:\n{str_gpt_res}")

                    cocktail_recipe = self.parse_gpt_message_to_cocktail_recipe(
                        str_gpt_res_cleaned)

                    ingredients = self.save_ingredients(cocktail_recipe)

                    recipe_id = self.save_recipe(cocktail_recipe, ingredients)

                    print(f"Ricetta salvata nel database con id: {recipe_id}")
                else:
                    print(
                        "\nErrore: La risposta generata non rispetta il formato richiesto.")
                    print("Risposta ricevuta:")
                    print(gpt_response.testo)
                    print(
                        "Si prega di riformulare il prompt o verificare eventuali errori.")


if __name__ == "__main__":
    bot = CocktailAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        connection_string=os.getenv("DB_CONNECTION_STRING"),
        db_name=os.getenv("DB_NAME")
    )

    # 2. Richiedi a GPT di generare la ricetta strutturata
    cocktail_name = "gin tonic"
    prompt_first = (
        f"Genera una ricetta strutturata per preparare un cocktail chiamato '{cocktail_name}'. "
        "La risposta deve essere formattata esattamente in questo modo:\n\n"
        "Ricetta per <NomeCocktail>:\n"
        "Ingredienti: <lista degli ingredienti separati da virgola>\n"
        "Preparazione: <descrizione della preparazione>\n\n"
        "Assicurati di rispettare il formato."
    )

    bot.pipeline_structured_output()
