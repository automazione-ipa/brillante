# proto.Message to pyadntic Mapping Usecase

## Descrizione

La `Piattaforma LayerAI` espone dei servizi di machine learning dei provider **Azure** e **Google**. 

Utilizza internamente dei `BaseModel` pydantic custom, creati sulla base delle classi dei provider e poi unificando richieste e risposte dove possibile.

Per quanto riguarda l'unificazione dei payload o di parti di esso, è difficile da automatizzare, inoltre le scelte a riguardo richiedono l'intervento umano e il lavoro del team di sviluppo.

Il lavoro di mapping iniziale invece è prevalentemente meccanico e può essere eseguito in automatico da un LLM.

Descriviamo ad esempio il caso del provider Google.

### proto.Message to pydantic

Si vuole automatizzare il processo di conversione da classi native Google a classi LayerAI.

Ad esempio, dato il modulo `document.py`, voglio generare un file `entities.py`; segue un esempio di conversione

```python
class ShardInfo(proto.Message):
    r"""For a large document, sharding may be performed to produce
    several document shards. Each document shard contains this field
    to detail which shard it is.

    Attributes:
        shard_index (int):
            The 0-based index of this shard.
        shard_count (int):
            Total number of shards.
        text_offset (int):
            The index of the first character in
            [Document.text][google.cloud.documentai.v1.Document.text] in
            the overall document global text.
    """

    shard_index: int = proto.Field(
        proto.INT64,
        number=1,
    )
    shard_count: int = proto.Field(
        proto.INT64,
        number=2,
    )
    text_offset: int = proto.Field(
        proto.INT64,
        number=3,
    )
```
diventa

```python
class ShardInfo(BaseModel):
    """
    Class representing a sharding may be performed to produce several document shards.

    Each document shard contains this field to detail which shard it is.
    """

    shard_index: int
    """The 0-based index of the current shard."""
    shard_count: int
    """Total number of shards."""
    text_offset: int
    """Text offset indicating the starting point of the shard in the document."""
```

Nella versione definitiva, potrei aggiungere in testa al file gli import necessari, nel nostro caso

```python
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel
```


## Function-call prevista

- `write_file(path: str, content: str) -> None`  
  Scrive su disco il contenuto `content` in `path`.

---

## Prompt previsto

> "Dato il seguente file `document.py`, voglio:  
> - ripulirlo da tutte le parti non necessarie per il mapping delle classi;  
> - generare una versione dove ogni classe `proto.Message` diventa una classe `BaseModel` Pydantic, mantenendo la docstring e i tipi dei campi;  
> - salvare il modulo localmente tramite una function call `write_file(path: str, content: str)`."

---

## Esempio di domanda prevista

- **"Dato il file document.py, creami il file entities.py con i BaseModel derivati dalle classi proto.Message."**


