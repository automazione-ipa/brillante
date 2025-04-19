from gpt_wrap import chat_with_openai

try:
    reply = chat_with_openai(
        user_message="""
        Provide information about an Italian region in JSON format with the following fields:
        - name
        - population
        - area_km2
        - capital
        - provinces (list)

        Example:
        Input: Lombardia
        Output: {
          "name": "Lombardia",
          "population": 10060574,
          "area_km2": 23844,
          "capital": "Milano",
          "provinces": ["Milano", "Bergamo", "Brescia", "Como", "Cremona", "Lecco", "Lodi", "Mantova", "Monza e Brianza", "Pavia", "Sondrio", "Varese"]
        }
        """,
        system_message='You are a helpful assistant.',
        temperature=0.5
    )
    print(reply)
except Exception as e:
    print(str(e))
