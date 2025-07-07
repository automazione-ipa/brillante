"""Dispatcher and registry for GPT-callable functions to handlers."""
from functions import FUNCTIONS
from travel_functions import (
    read_file,
    write_file,
    generate_schema,
    search_images,
    fetch_prices,
    build_report
)


class FunctionRegistry:
    def __init__(self):
        self._registry = {}
        # register core functions
        self.register(read_file, next(f for f in FUNCTIONS if f['name'] == 'read_file'))
        self.register(write_file, next(f for f in FUNCTIONS if f['name'] == 'write_file'))
        # register travel-specific
        self.register(generate_schema, next(f for f in FUNCTIONS if f['name'] == 'generate_itinerary_schema'))
        self.register(search_images, next(f for f in FUNCTIONS if f['name'] == 'search_images'))
        self.register(fetch_prices, next(f for f in FUNCTIONS if f['name'] == 'fetch_prices'))
        self.register(build_report, next(f for f in FUNCTIONS if f['name'] == 'build_report'))

    def register(self, handler, definition: dict):
        """
        Register a function handler with its GPT definition.
        """
        self._registry[definition['name']] = {
            'definition': definition,
            'handler': handler
        }

    def get_definition(self):
        """Return list of all function definitions."""
        return [v['definition'] for v in self._registry.values()]

    def call(self, name: str, args: dict):
        """Invoke handler by name with parsed args."""
        entry = self._registry.get(name)
        if not entry:
            raise ValueError(f"Function {name} not registered.")
        return entry['handler'](**args)


# Instantiate global registry
function_registry = FunctionRegistry()
