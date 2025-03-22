# Fibonacci Implementations in MathAgent

This project provides two implementations of the Fibonacci sequence inside the `MathAgent` class:

## Recursive Version
The `fibonacci_recursive(n)` function calculates the Fibonacci sequence using recursion. This approach is simple but inefficient for large values of `n` due to redundant calculations.

**Usage:**
```python
MathAgent.fibonacci_recursive(n)
```

## Iterative Version
The `fibonacci_iterative(n)` function generates the Fibonacci sequence using an iterative approach, storing values in a list. This method is more efficient in terms of performance and avoids excessive function calls.

**Usage:**
```python
MathAgent.fibonacci_iterative(n)
```

## Example Output
```
Iterative Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
Recursive Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

Use the iterative version for better performance, especially when working with larger values of `n`.

## Funzionamento in dettaglio
Vediamo in dettaglio il funzionamento di questo `for`:

```python
for i in range(2, n):
    fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
return fib_sequence[:n]
```

### **Spiegazione passo passo**

1. **`range(2, n)`**  
   - Il ciclo `for` inizia da `i = 2` e continua fino a `n - 1`.  
   - Non parte da `0` o `1` perché i primi due numeri della sequenza di Fibonacci (`0, 1`) sono già definiti nella lista `fib_sequence = [0, 1]`.

2. **`fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])`**  
   - `fib_sequence[-1]` prende l'ultimo numero nella lista (il più recente).  
   - `fib_sequence[-2]` prende il penultimo numero.  
   - Si sommano questi due numeri per ottenere il nuovo numero della sequenza.  
   - Il risultato viene aggiunto alla lista `fib_sequence` con `append()`.

3. **Esempio pratico con `n = 10`**  

   - `fib_sequence` inizia come `[0, 1]`
   - Iterazione `i = 2`: `1 + 0 = 1` → `[0, 1, 1]`
   - Iterazione `i = 3`: `1 + 1 = 2` → `[0, 1, 1, 2]`
   - Iterazione `i = 4`: `2 + 1 = 3` → `[0, 1, 1, 2, 3]`
   - Iterazione `i = 5`: `3 + 2 = 5` → `[0, 1, 1, 2, 3, 5]`
   - Iterazione `i = 6`: `5 + 3 = 8` → `[0, 1, 1, 2, 3, 5, 8]`
   - Iterazione `i = 7`: `8 + 5 = 13` → `[0, 1, 1, 2, 3, 5, 8, 13]`
   - Iterazione `i = 8`: `13 + 8 = 21` → `[0, 1, 1, 2, 3, 5, 8, 13, 21]`
   - Iterazione `i = 9`: `21 + 13 = 34` → `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`

4. **`return fib_sequence[:n]`**  
   - `[:n]` assicura che la lista restituita contenga esattamente `n` elementi, anche se l'input fosse piccolo.

### **Conclusione**
Questo `for` costruisce in modo efficiente la sequenza di Fibonacci evitando chiamate ricorsive ripetute, rendendola molto più veloce rispetto alla versione ricorsiva. 🚀


## Ottimizzare il caso ricorsivo con memoization
La **memoization** è una tecnica di ottimizzazione che consiste nel **salvare i risultati** delle chiamate a funzioni in modo che, quando la stessa funzione è chiamata con gli stessi argomenti, il risultato venga **riutilizzato** invece di essere ricalcolato. Questo approccio è particolarmente utile in problemi ricorsivi, dove lo stesso valore potrebbe essere calcolato ripetutamente in diverse chiamate ricorsive.

### Funzionamento della **memoization**:

1. **Memorizzazione dei risultati**: Ogni volta che una funzione viene chiamata, il risultato per una specifica combinazione di argomenti viene **salvato** (ad esempio in un dizionario).
2. **Riutilizzo dei risultati**: Se la funzione viene chiamata di nuovo con gli stessi argomenti, **il valore memorizzato** viene restituito immediatamente, evitando il ricalcolo.

Nel caso del decoratore `@lru_cache`:
- **`maxsize=None`**: La cache può crescere senza limiti (puoi anche specificare un numero per limitare la dimensione della cache).
- La cache memorizza i risultati delle funzioni in base ai loro argomenti, così da evitare calcoli ridondanti.

### Vantaggi:
- **Migliora l'efficienza** nelle funzioni ricorsive, riducendo il numero di chiamate ripetute.
- **Aumenta la velocità** e **riduce il tempo di esecuzione**.

### Esempio:
Se chiami `fibonacci_memo(10)`, il risultato per `fibonacci_memo(9)` e `fibonacci_memo(8)` verrà memorizzato, quindi chiamandoli di nuovo non verranno ricalcolati.