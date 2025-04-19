import os
from dotenv import load_dotenv
from agents.openai.chat_agent import ChatAgent

load_dotenv()


def main():
    # Instantiate the ChatAgent with your API key and desired model
    keyword = os.environ.get("OPENAI_API_KEY")
    print(keyword)
    chat = ChatAgent(api_key=keyword, model="gpt-4o")

    topic = "ETHEREUM CRYPTO DAOs: caso studio su YEARN FINANCE ed $YFI"
    prompt = f"Genera un tweet coinvolgente e conciso sull'argomento: {topic}"

    # Generate the tweet (streaming is optional; here we use non-streaming)
    tweet = chat.generate_tweet(prompt=prompt)
    print(f"\nTweet generato:\n{tweet.testo}")


if __name__ == "__main__":
    main()
