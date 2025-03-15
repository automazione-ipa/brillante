from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci_memo(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)

# salvo il risultato di una combinazione chiamante , ad esempio in un dizionario
# posso riutilizzare il risultato senza calcolarlo di nuovo, evitando molti calcoli inutili