from gpt_wrap.gpt_wrap import chat_functions

def summarize_text(chunk: str, system_msg: str = None) -> str:
    """
    Prende un pezzo di testo e ne restituisce un riassunto conciso.
    """
    prompt = (
        "Riassumi in modo chiaro e conciso il seguente testo:\n\n"
        f"{chunk}"
    )
    resp = chat_functions(
        user_message=prompt,
        system_message=system_msg or "Sei un modello che fa riassunti precisi e sintetici.",
        temperature=0.3
    )
    
    return resp['choices'][0]['message']['content']
