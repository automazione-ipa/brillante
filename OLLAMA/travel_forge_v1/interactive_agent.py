"""ChatAgent orchestrator for itinerary generation."""
import logging, json
from gpt_wrap import chat_functions, gpt_choice_message
from helpers import function_registry

logger = logging.getLogger(__name__)


class ItineraryAgent:
    """Agent for collaborative function-calling itinerary generation."""
    def __init__(self):
        self.history = []

    def ask_generate_schema(self, city_country: str, duration_days: int, season_or_dates: dict):
        prompt = (
            f"Prepara uno schema di massima per un viaggio a {city_country} "
            f"per {duration_days} giorni nel periodo {season_or_dates}."
        )
        response = chat_functions(
            user_message=prompt,
            functions=function_registry.get_definition(),
            function_call="auto"
        )
        msg = gpt_choice_message(response)
        if not msg.get('function_call'):
            raise RuntimeError("GPT non ha invocato alcuna funzione di schema.")
        return msg['function_call']

    def handle_function_call(self, function_call: dict):
        name = function_call['name']
        args = json.loads(function_call['arguments'])
        logger.info(f"Calling function {name} with args {args}")
        result = function_registry.call(name, args)
        # add function response to history
        self.history.append({'role': 'function', 'name': name, 'content': json.dumps(result)})
        return result

    def run(self, city_country: str, duration_days: int, season_or_dates: dict):
        # Step 1: generate schema
        func_call = self.ask_generate_schema(city_country, duration_days, season_or_dates)
        schema = self.handle_function_call(func_call)
        # Step 2: images
        image_call = {
            'name': 'search_images',
            'arguments': json.dumps({'keywords': [step['activity'] for step in schema['itinerary']]})
        }
        images = self.handle_function_call(image_call)
        # Step 3: prices
        price_call = {
            'name': 'fetch_prices',
            'arguments': json.dumps({'itinerary': schema['itinerary'], 'dates': season_or_dates})
        }
        prices = self.handle_function_call(price_call)
        # Step 4: report
        report_call = {
            'name': 'build_report',
            'arguments': json.dumps({
                'city': city_country,
                'dates': season_or_dates,
                'itinerary': schema['itinerary'],
                'images': images,
                'prices': prices
            })
        }
        markdown = self.handle_function_call(report_call)
        return markdown
