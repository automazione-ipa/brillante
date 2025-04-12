from gpt_wrap import chat_with_openai


def gpt_grammar_check(text: str):
    """Applica controllo grammaticale e restituisce il testo corretto."""
    return chat_with_openai(
        user_message=f"Correggi il seguente testo: {text}",
        system_message="Sei un correttore grammaticale che corregge testi mantenendo il significato originale.",
        temperature=0.2
    )


incorrect_text = 'Io avere andato al mercato ieri.'
res = gpt_grammar_check(incorrect_text)

print(res)
