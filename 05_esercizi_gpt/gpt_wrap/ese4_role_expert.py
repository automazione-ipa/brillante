from gpt_wrap import chat_with_openai

try:
    reply = chat_with_openai(
        user_message="""
        Act as a travel expert. Help the client plan a trip by asking relevant questions and providing useful suggestions.
        """,
        system_message='You are a helpful assistant.',
        temperature=0.5
    )
    print(reply)
except Exception as e:
    print(str(e))
