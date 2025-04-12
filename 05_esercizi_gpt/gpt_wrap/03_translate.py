from gpt_wrap import chat_with_openai


def translate(text: str, system_msg: str):
    """Applica controllo grammaticale e restituisce il testo corretto."""
    return chat_with_openai(
        user_message=f"Traduci in francese: '{text}'",
        system_message=system_msg,
        temperature=0.3
    )


res = translate(
    text="Buongiorno, come stai?",
    system_msg="Sei un traduttore esperto che traduce accuratamente testi tra diverse lingue."
)

print(res)



