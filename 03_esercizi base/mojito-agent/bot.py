import os
from dotenv import load_dotenv

from db.db_core import DBCore
from openai_agent.chat_agent import ChatAgent

load_dotenv()


class CocktailAgent:
    def __init__(self):
        pass

    def is_valid_recipe(self, recipe: str) -> bool:
        """
        Verifica se la risposta ottenuta da GPT rispetta il formato atteso.
        Ad esempio, controlla che contenga le sezioni 'Ingredienti:' e 'Preparazione:'.
        """
        return "Ingredienti:" in recipe and "Preparazione:" in recipe


def main():
    db_core = DBCore(
        connection_string=os.getenv("DB_CONNECTION_STRING"),
        db_name=os.getenv("DB_NAME")
    )
    chat = ChatAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )
    cocktail_agent = CocktailAgent()

    while True:
        print("\n=== Ricerca o generazione ricetta per cocktail ===")
        cocktail_name = input("Inserisci il nome di un cocktail (es. mojito, margarita, negroni) o 'exit' per uscire: ").strip().lower()
        if cocktail_name == "exit":
            print("Arrivederci!")
            break

        recipe = db_core.get_cocktail_recipe(cocktail_name)
        if recipe:
            print(f"\nRicetta trovata nel database per {cocktail_name.capitalize()}:\n{recipe}")
        else:
            print(f"\nNessuna ricetta trovata per {cocktail_name.capitalize()} nel database.")
            # 2. Richiedi a GPT di generare la ricetta strutturata
            prompt = (
                f"Genera una ricetta strutturata per preparare un cocktail chiamato '{cocktail_name}'. "
                "La risposta deve essere formattata esattamente in questo modo:\n\n"
                "Ricetta per <NomeCocktail>:\n"
                "Ingredienti: <lista degli ingredienti separati da virgola>\n"
                "Preparazione: <descrizione della preparazione>\n\n"
                "Assicurati di rispettare il formato."
            )
            gpt_response = chat.generate_response(prompt)

            if cocktail_agent.is_valid_recipe(gpt_response):
                print(f"\nRicetta generata da GPT per {cocktail_name.capitalize()}:\n{gpt_response}")
                recipe_id = db_core.save_cocktail_recipe(cocktail_name, gpt_response)
                print(f"Ricetta salvata nel database con id: {recipe_id}")
            else:
                print("\nErrore: La risposta generata non rispetta il formato richiesto.")
                print("Risposta ricevuta:")
                print(gpt_response)
                print("Si prega di riformulare il prompt o verificare eventuali errori.")


if __name__ == "__main__":
    main()
