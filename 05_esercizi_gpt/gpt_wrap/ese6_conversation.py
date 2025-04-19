from gpt_wrap import chat_with_openai


def start_conversation():
    system_message = 'You are a helpful assistant.'

    print("Inizia la conversazione con GPT. Scrivi 'exit' per terminare.")

    while True:
        user_message = input("Tu: ")

        if user_message.lower() == 'exit':
            print("Conversazione terminata.")
            break

        try:
            reply = chat_with_openai(
                user_message=user_message,
                system_message=system_message,
                temperature=0.5
            )
            print(f"GPT: {reply}")
        except Exception as e:
            print(f"Errore: {str(e)}")


if __name__ == "__main__":
    start_conversation()
