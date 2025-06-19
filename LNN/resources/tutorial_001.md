### **Rappresentazione della Conoscenza con Predicati (LNN)**

* **Predicati**: Sono i blocchi fondamentali della logica del primo ordine nei sistemi come le **Logical Neural Networks (LNNs)**.

  * **Predicati unari**: descrivono proprietà di oggetti (es. `Smokes(x)` indica se x fuma).
  * **Predicati n-ari** (n > 1): descrivono relazioni tra oggetti (es. `Friends(x, y)` indica se x e y sono amici).

* **Arity**: Indica il numero di argomenti del predicato (es. `arity=2` per relazioni binarie).

* **Grounding**: Ogni combinazione di input (cioè ogni riga della tabella di verità) rappresenta un'istanza concreta del predicato, detta **grounding**.

* **Verità**: A ogni riga (grounding) è associato un valore di verità.

* **Definizione in codice (LNN)**:

  ```python
  from lnn import Predicates

  Smokes, Cancer = Predicates('Smokes', 'Cancer')  # predicati unari
  Friends = Predicates('Friends', arity=2)         # predicato binario
  ```

* **Nome**: Ogni predicato deve avere un nome identificativo usato all'interno del modello.

---

Questo sistema consente di rappresentare conoscenza strutturata logicamente e assegnare valori di verità a fatti concreti nel contesto di modelli logici neurali.


## Query Setup (first try, got errors)


```python
# 1. Inseriamo la query esplicita su Smokes(Bob)
bob_smokes = Smokes('Bob')
logger.info(f"✨ Query: qual è lo stato di {bob_smokes}?")

# Registriamo la query nel modello e forziamo la convergenza alla sua radice
model.set_query(bob_smokes, world=None, converge=True)

# 2. Inferenza focalizzata sulla query
state_bounds, _ = model.infer_query()
lower, upper = state_bounds
logger.info(f"💡 Risultato per Smokes(Bob): truth interval = [{lower:.2f}, {upper:.2f}]")

# 3. (Opzionale) Anche un infer controllo completo
logger.info("Stato corrente per nodo query:")
node = model[bob_smokes]
logger.info(f"- Nodo formula: {node.formula}")
logger.info(f"- Intervallo di verità: [{node.state.lower:.2f}, {node.state.upper:.2f}]")

logger.info("✅ Query eseguita con successo!")
```

