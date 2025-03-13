import json


class QueryData:

    @staticmethod
    def get_query_data(value_path):
        """Extract the first query from the validation data."""
        with open(value_path) as f:
            data = json.load(f)

        return data[0]['question']

    @staticmethod
    def get_reference_answer(value_path):
        with open(value_path) as f:
            data = json.load(f)

        return data[0]['ideal_answer']

