
def calculate(expression: str) -> dict:
    """
    Valuta un'espressione matematica e restituisce un dict con il risultato.
    """
    try:
        # Attenzione: eval() può eseguire codice arbitrario. Assicurarsi di
        # validare o filtrare l'input in contesti di produzione.
        result = eval(expression, {"__builtins__": None}, {})
    except Exception as e:
        return {"error": str(e)}
    return {"result": result}
