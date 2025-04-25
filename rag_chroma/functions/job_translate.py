from gpt_wrap.gpt_wrap import chat_functions


def translate(text: str, system_msg: str):
    """Applica controllo grammaticale e restituisce il testo corretto."""
    return chat_functions(
        user_message=f"Traduci in francese: '{text}'",
        system_message=system_msg,
        temperature=0.3
    )


res = translate(
    text="Buongiorno, come stai?",
    system_msg="Sei un traduttore esperto che traduce accuratamente testi tra diverse lingue."
)

print(res)
