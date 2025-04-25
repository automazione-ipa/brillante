from gpt_wrap.gpt_wrap import get_embedding

embedding = get_embedding(
    text="L'intelligenza artificiale sta rivoluzionando il mondo della tecnologia."
)
print("Embedding del testo:")
print(embedding)