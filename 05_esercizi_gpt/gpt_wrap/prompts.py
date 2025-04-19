# prompts.py

zero_shot_prompt = "What are the capitals of France, Japan, and Australia?"

few_shot_prompt = """
Provide information about an Italian region in JSON format with the following fields:
- name
- population
- area_km2
- capital
- provinces (list)
"""

cot_prompt = """
Calculate the first 10 Fibonacci numbers. Explain each step before giving the result.
"""

role_expert_prompt = """
Act as a travel expert. Help the client plan a trip by asking relevant questions and providing useful suggestions.
"""
