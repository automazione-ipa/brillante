from gpt_wrap import chat_with_openai

try:
    reply = chat_with_openai(
        user_message='What are the capitals of France, Japan, and Australia?',
        system_message='You are a helpful assistant.',
        temperature=0.5
    )
    print(reply)
except Exception as e:
    print(str(e))
