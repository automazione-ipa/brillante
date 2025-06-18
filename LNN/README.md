# 🧠 Progetto: Ragionamento Giuridico con LNN

This guide provides a concise reference to using the IBM Logical Neural Networks (LNN) library (2023 version). It covers model setup, adding knowledge and data, inference, and key constants/enums.

## 1. Introduzione - LNN Cookbook Guide (IBM LNN Latest Version)
Utilizziamo **Logical Neural Networks (LNN)**, un framework **neuro‑simbolico** che unisce capacità di apprendimento automatico con rigore logico.  
Ogni neurone corrisponde a un costrutto logico pesato — con:
- Inferenza bidirezionale (forward/backward reasoning)
- Modello end‑to‑end differenziabile
- Gestione dell'incertezza tramite intervalli di verità
- Resilienza a conoscenza incompleta o inconsistenti

---

### 1. Installation

```bash
pip install git+https://github.com/IBM/LNN.git
```

---

### 2. Creating a Dynamic LNN Model

```python
from lnn import Model

# Initialize an empty model
g_model = Model()
```

A `Model` is a container for logical formulae, data, and inference state; it is populated on-demand.

---

### 3. Defining Variables and Predicates

```python
from lnn import Variables, Predicates

# First-order logic variables
x, y = Variables('x', 'y')

# Predicates (specify arity for relations)
Smokes, Cancer = Predicates('Smokes', 'Cancer')  # unary predicates
Friends = Predicates('Friends', arity=2)
```

---

### 4. Adding Knowledge (Axioms)

Use `add_knowledge` to insert formulae (axioms) into the model under a chosen world assumption.

```python
from lnn import Implies, Iff, World

# Logical rules
rule1 = Implies(Smokes(x), Cancer(x))
rule2 = Implies(Friends(x, y), Iff(Smokes(x), Smokes(y)))

# Add as axioms (always true)
g_model.add_knowledge(rule1, rule2, World.AXIOM)
```

* **World.AXIOM**: formulae assumed universally true.
* **World.OPEN**, **World.CLOSED**, **World.CONTRADICTION** available.

---

### 5. Adding Data (Facts/Beliefs)

Raw facts or belief bounds must be added via `add_data` (not deprecated `add_facts`).

```python
from lnn import Fact

g_model.add_data({
    Smokes: { 'Alice': Fact.TRUE },
    Friends: { ('Alice', 'Bob'): Fact.TRUE }
})
```

* For **propositional** formulae, map `Formula: Fact.TRUE/FALSE/UNKNOWN` or numeric bounds.
* For **FOL** predicates, provide a dict keyed by grounding tuples/strings.

---

### 6. Running Inference

After data and axioms are loaded, call:

```python
g_model.infer()
```

This executes upward and downward passes to propagate truth bounds.

---

### 7. Inspecting Results

Access node states via model indexing:

```python
alice_cancer = g_model['Cancer(Alice)']
bob_smokes = g_model['Smokes(Bob)']
print(alice_cancer.state, bob_smokes.state)
```

Use `model.items()` to list all formula states.

---

### 8. Key Constants and Enums (constants.py)

#### 8.1 `Fact` enum

* `Fact.TRUE = (1.0, 1.0)` – definitely true
* `Fact.FALSE = (0.0, 0.0)` – definitely false
* `Fact.UNKNOWN = (0.0, 1.0)` – unknown
* `Fact.CONTRADICTION = (1.0, 0.0)` – conflicting evidence

#### 8.2 `_AutoName` base class

Used to auto-generate string-valued enum members.

#### 8.3 `Bound` enum

* `Bound.LOWER`, `Bound.UPPER` restrict inference to lower/upper truth bound.

#### 8.4 `Direction` enum

* `Direction.UPWARD`, `Direction.DOWNWARD` control inference pass direction.

#### 8.5 `Join` enum

* `Join.INNER`, `INNER_EXTENDED`, `OUTER`, `OUTER_PRUNED` for grounding joins.

#### 8.6 `Loss` enum

* `Loss.LOGICAL`, `SUPERVISED`, `UNCERTAINTY`, `CONTRADICTION`, `CUSTOM` for training.

#### 8.7 `NeuralActivation` enum

* `Godel`, `Frechet`, `Lukasiewicz`, `LukasiewiczTransparent`, `Product` for t-norm choices.

#### 8.8 `World` enum

* `World.AXIOM` (1.0,1.0), `OPEN` (0.0,1.0), `CLOSED`/`FALSE` (0.0,0.0), `CONTRADICTION` (1.0,0.0).

---

### 9. Best Practices

* Use **`add_knowledge`** strictly for inserting logical formulae (axioms, rules).
* Use **`add_data`** for ground facts and beliefs; keys must match existing formula objects.
* Always call **`infer()`** after adding data to propagate bounds.
* Inspect **`model[...] .state`** or `model.items()` for results.

---

This guide aligns with the latest IBM LNN (2023) API. It should serve as a quick-reference for building and reasoning with logical neural networks.

---

## 2. Regolamenti e Ragionamenti In Ambito Giuridico

**Perché può essere utile applicare questi concetti in ambito giuridico?**
- **Spiegazioni logiche trasparenti**
- **Rappresentazione di norme, fatti e deduzioni complesse**
- **Scalabilità verso grandi KB normative**

---

### Introduzione

Modellato formalmente:

* Un americano che vende armi a una nazione ostile è criminale
* Fatti: `West`, `Nono`, `M1`
* Risultato: inferenza `West` → criminale
  Codice LNN con `Forall`, `Exists`, `Predicate`, `Fact`.

---

## 3. Paper recenti & integrazione per il diritto

### 📘 Neural Reasoning Networks (AAAI 2025)

* Architettura LNN migliorata con logica di **Lukasiewicz**, ottimizzazione strutturale e spiegazioni testuali interpretabili ([arxiv.org][1], [github.com][2])
* Prestazioni competitive con modelli ML classici e training 43 % più veloce ([arxiv.org][3])

**Implicazione legale:**
Generazione di spiegazioni testuali logiche facilmente interpretabili da avvocati o giudici.

---

### 📗 Neuro‑Symbolic ILP con LNN (AAAI 2022)

* Estensione di LNN per apprendimento di regole FOL da dati rumorosi ([ojs.aaai.org][4])
* Regole interpretabili e accurate (>98 %), utili per estrazione automatica da sentenze legali.

---

### 🔗 Estensione FOL & RL

* Supporto funzioni, uguaglianza, regole non lineari e reinforcement learning con memoria logica&#x20;
* Fondamentale per modellare norme equivalenti, soglie risarcitorie e percorsi processuali sequenziali.

---

## 4. Roadmap & obiettivi

| Tema                         | Obiettivo giuridico                                             |
| ---------------------------- | --------------------------------------------------------------- |
| 🧾 **Spiegazioni logiche**   | Rendere leggibili le "motivazioni" delle decisioni giudiziarie  |
| 🧰 **Completamento KB**      | Scoprire norme implicite e clausole da testi giuridici          |
| 🧮 **Norme non lineari**     | Modellare soglie, penalità proporzionali, carenze risarcitorie  |
| 📚 **Estrazione automatica** | Derivare regole da corpora di sentenze e contratti              |
| 🔄 **Workflow sequenziale**  | Usare RL con memoria logica per simulare iterazioni processuali |

---

## 5. Pipeline proposta

1. **NRN (AAAI 2025)**: generazione di spiegazioni testuali integrate.
2. **LNN‑ILP (AAAI 2022)**: estrazione di regole normative da dataset giuridici.
3. **FOL‑extensions**: modellare uguaglianze, soglie, equivalenze.
4. **RL logico sequenziale**: simulare processi passo‑per‑passo nei tribunali.

---

## 6. Setup e ambientazione

```bash
conda create -n lnn python=3.9 -y
conda activate lnn
pip install git+https://github.com/IBM/LNN.git
```

---

## 7. Prossimi passi

* **Implementare** snippet NRN con spiegazioni testuali
* **Testare** pipeline ILP su dataset legali (es. sentenze italiane)
* **Integrare** supporto södl per funzioni/uguaglianza
* **Prototipare** RL per simulazioni processuali

---

## 📚 Risorse utili

* **LNN GitHub** – framework LNN base ([research.ibm.com][5], [ojs.aaai.org][4], [research.ibm.com][6], [github.com][2])
* **NRN AAAI 2025** – spiegazioni testuali su LNN ([research.ibm.com][7])
* **LNN‑ILP AAAI 2022** – estrazione regole FOL&#x20;

---

## ✅ Conclusione

Abbiamo una solida base (geometria, regole giuridiche), una roadmap chiara con paper all'avanguardia e una direzione precisa: integrare spiegazioni testuali, estrazione automatica e processi sequenziali per il ragionamento giuridico.
Ora tocca a noi implementare, testare e iterare verso una piattaforma ILP-Giuridica evoluta.

> **Prossimo passo:** definire un caso d'uso legale concreto e iniziare a modellarlo con LNN+NRN.


Fammi sapere quando lo inserisco nel repository ufficiale oppure se desideri modifiche o approfondimenti su sezioni specifiche!


[1]: https://arxiv.org/html/2410.07966v1?utm_source=chatgpt.com "Neural Reasoning Networks: Efficient Interpretable Neural Networks With ..."
[2]: https://github.com/IBM/LNN?utm_source=chatgpt.com "GitHub - IBM/LNN: A `Neural = Symbolic` framework for sound and ..."
[3]: https://ibm.github.io/neuro-symbolic-ai/blog/nsai-wkshp-2023-blog/ "IBM Badge"
[4]: https://arxiv.org/abs/2410.07966?utm_source=chatgpt.com "Neural Reasoning Networks: Efficient Interpretable Neural Networks With Automatic Textual Explanations"
[5]: https://ojs.aaai.org/index.php/AAAI/article/view/20795?utm_source=chatgpt.com "Neuro-Symbolic Inductive Logic Programming with Logical Neural Networks"
[6]: https://research.ibm.com/topics/neuro-symbolic-ai?utm_source=chatgpt.com "Neuro-symbolic AI - IBM Research"
[7]: https://research.ibm.com/publications/neuro-symbolic-inductive-logic-programming-with-logical-neural-networks?utm_source=chatgpt.com "Neuro-Symbolic Inductive Logic Programming with Logical Neural Networks ..."
[8]: https://research.ibm.com/projects/extensions-and-nlu-applications-of-logical-neural-networks?utm_source=chatgpt.com "Extensions and NLU Applications of Logical Neural Networks"
[9]: https://github.com/IBM/neuro-symbolic-ai "IBM Neural Networks"