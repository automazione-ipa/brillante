import json
from gpt_wrap import chat_functions, gpt_choice_message
from travel_forge_v1.helpers import function_registry
from travel_forge_v1.entities import ItineraryRequest


class ItineraryService:

    async def create_itinerary(self, request: ItineraryRequest) -> str:
        user_prompt = (
            f"Prepara uno schema di massima per un viaggio a {request.city_country} "
            f"per {request.duration_days} giorni nel periodo {request.season_or_dates}."
        )

        # Step 1: Ask GPT to call the itinerary schema function
        response = chat_functions(
            user_message=user_prompt,
            functions=function_registry.get_definition(),
            function_call="auto"
        )
        msg = gpt_choice_message(response)

        if not msg.get("function_call"):
            raise RuntimeError("GPT non ha invocato la funzione generate_itinerary_schema")

        fn_call = msg["function_call"]
        args = json.loads(fn_call["arguments"])

        # Step 2: Generate itinerary schema
        itinerary_data = function_registry.call(fn_call["name"], args)

        # Step 3: Search images
        keywords = [step['activity'] for step in itinerary_data['itinerary']]
        images = function_registry.call("search_images", {"keywords": keywords})

        # Step 4: Fetch prices
        prices = function_registry.call("fetch_prices", {
            "itinerary": itinerary_data['itinerary'],
            "dates": request.season_or_dates.dict()
        })

        # Step 5: Build final markdown report
        markdown = function_registry.call("build_report", {
            "city": request.city_country,
            "dates": request.season_or_dates.dict(),
            "itinerary": itinerary_data['itinerary'],
            "images": images,
            "prices": prices,
        })

        return markdown
