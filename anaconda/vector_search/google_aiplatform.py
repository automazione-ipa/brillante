# CONSTANTS MODULE
from enum import Enum
from uuid import uuid4
from typing import List, Optional, Union, Any, Dict

from pydantic import BaseModel, Field
from google.cloud.aiplatform_v1.types import IndexDatapoint as GCPIndexDatapoint
from google.cloud.aiplatform import MatchingEngineIndex
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials


# from HuggingFace
from sentence_transformers import SentenceTransformer


class Operator(Enum):
    """Which comparison operator to use for numeric restrictions."""

    OPERATOR_UNSPECIFIED = 0
    LESS = 1
    LESS_EQUAL = 2
    EQUAL = 3
    GREATER_EQUAL = 4
    GREATER = 5
    NOT_EQUAL = 6


class SparseEmbedding(BaseModel):
    """Feature embedding vector for sparse index. An array of numbers whose values are located in the specified dimensions."""

    values: List[float]
    """Required. The list of embedding values of the sparse vector."""
    dimensions: List[int]
    """Required. The list of indexes for the embedding values of the sparse vector."""


class Restriction(BaseModel):
    """Restriction of a datapoint which describe its attributes (tokens) from each of several attribute categories (namespaces)."""

    namespace: str
    """The namespace of this restriction. e.g.: color."""
    allow_list: Optional[List[str]] = None
    """The attributes to allow in this namespace. e.g.: 'red'"""
    deny_list: Optional[List[str]] = None
    """The attributes to deny in this namespace. e.g.: 'blue'"""


class NumericRestriction(BaseModel):
    """Allows restricting datapoints based on numeric comparisons rather than categorical tokens. Only one of the value fields should be set."""

    namespace: str
    """The namespace of this restriction. e.g.: cost."""
    op: Operator
    """The comparison operator to apply."""
    value: Optional[Union[int, float]] = None
    """Represents 64 bit integer or 32/64 bit float"""


class CrowdingTag(BaseModel):
    """Constraint on neighbor lists produced by nearest neighbor search, limiting number of neighbors per attribute value."""

    crowding_attribute: str
    """The attribute value used for crowding. The maximum number of neighbors 
    to return per crowding attribute value is configured per-query."""


class IndexDatapoint(BaseModel):
    """A datapoint for an index, containing dense and optional sparse embeddings,
    as well as optional restrictions and crowding tags."""

    datapoint_id: str
    """Required. Unique identifier of the datapoint."""
    feature_vector: List[float]
    """Required. Feature embedding vector for dense index. An array of floats of
     length matching the configured dimensions."""
    sparse_embedding: Optional[SparseEmbedding] = None
    """Optional. Feature embedding vector for sparse index."""
    restricts: Optional[List[Restriction]]= None
    """Optional. List of categorical restrictions for performing filtered searches."""
    numeric_restricts: Optional[List[NumericRestriction]] = None
    """Optional. List of numeric restrictions for performing filtered searches."""
    crowding_tag: Optional[CrowdingTag] = None
    """Optional. Crowding tag to limit returned neighbors per attribute value."""


class ArticleMetadata(BaseModel):
    sezione: str
    anno: int
    tipo: str
    note: Optional[str] = None


class Article(BaseModel):
    numero: str
    titolo: str
    testo: str
    metadata: ArticleMetadata
    datapoint_id: str = Field(default_factory=lambda: str(uuid4()))
    embedding: Optional[List[float]] = None


# --- 1) Definizione dei primi articoli costituzionali con metadati ---
articolo_1 = Article(
    numero="1",
    titolo="Principi fondamentali",
    testo=(
        "L'Italia è una Repubblica democratica, fondata sul lavoro. "
        "La sovranità appartiene al popolo, che la esercita nelle forme e nei limiti della Costituzione."
    ),
    metadata=ArticleMetadata(
        sezione="Principi fondamentali",
        anno=1948,
        tipo="articolo",
        note="Articolo cardine"
    )
)

articolo_2 = Article(
    numero="2",
    titolo="Diritti inviolabili",
    testo=(
        "La Repubblica riconosce e garantisce i diritti inviolabili dell'uomo, sia come singolo sia nelle formazioni sociali "
        "ove si svolge la sua personalità, e richiede l'adempimento dei doveri inderogabili di solidarietà politica, economica e sociale."
    ),
    metadata=ArticleMetadata(
        sezione="Principi fondamentali",
        anno=1948,
        tipo="articolo"
    )
)

articolo_3 = Article(
    numero="3",
    titolo="Uguaglianza",
    testo=(
        "Tutti i cittadini hanno pari dignità sociale e sono eguali davanti alla legge "
        "senza distinzione di sesso, di razza, di lingua, di religione, di opinioni politiche, di condizioni personali e sociali."
        "E` compito della Repubblica rimuovere gli ostacoli di ordine economico e sociale, che, limitando di fatto la libertà e l'eguaglianza dei cittadini, impediscono il pieno sviluppo della persona umana e l'effettiva partecipazione di tutti i lavoratori all'organizzazione politica, economica e sociale del Paese."
    ),
    metadata=ArticleMetadata(
        sezione="Principi fondamentali",
        anno=1948,
        tipo="articolo"
    )
)

model = SentenceTransformer("all-mpnet-base-v2")


def transform_value(value: Any, parent_key: str = "") -> Any:
    if isinstance(value, Enum):
        return value.value
    elif isinstance(value, dict):
        return {
            (k if not (
                    parent_key == "numeric_restricts" and k == "value") else "value_double"):
                transform_value(v, parent_key)
            for k, v in value.items()
        }
    elif isinstance(value, list):
        return [transform_value(item, parent_key) for item in value]
    else:
        return value


def transform_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, value in data.items():
        if key == "numeric_restricts" and isinstance(value, list):
            result[key] = [transform_value(item, "numeric_restricts") for item
                           in value]
        else:
            result[key] = transform_value(value, key)
    return result


def get_embedding(text: str) -> List[float]:
    """
    Genera un embedding da 768 dimensioni per il testo dato.

    :param text: testo di input
    :return: lista di float (embedding)
    """
    emb = model.encode(text)
    return emb.tolist()

# Example
# embedding = get_embedding("Questo è un esempio.")
# print(len(embedding))
# print(embedding[:5])


# --- 2) Genera embedding per ciascun articolo ---

articoli: List[Article] = [articolo_1, articolo_2, articolo_3]
for art in articoli:
    art.embedding = model.encode(art.testo).tolist()
    print(f"[OK] Articolo {art.numero}: embedding dim = {len(art.embedding)}")
    print(f"Metadata: {art.metadata.dict()}")
    print("---")

# --- 4) Costruisci la lista di IndexDatapoint per l’upsert ---

dps: List[GCPIndexDatapoint] = []
for art in articoli:
    # Mappa Article → IndexDatapoint (our Pydantic BaseModel)
    idx_dp = IndexDatapoint(
        datapoint_id=art.datapoint_id,
        feature_vector=art.embedding,
        # esempio di restrizione categoriale su numero
        restricts=[Restriction(namespace="articolo", allow_list=[art.numero])],
        crowding_tag=CrowdingTag(crowding_attribute="costituzione")
    )
    dct = transform_dict(idx_dp.model_dump())
    dps.append(GCPIndexDatapoint(**dct))


# --- 5) (Opzionale) Stampa i primi 2 dps per verifica ---
for i, dp in enumerate(dps[:2], start=1):
    print(f"\n--- DP#{i} ---")
    print(dp)

# --- 6) (Opzionale) Upsert su Matching Engine ---
# creds = service_account.Credentials.from_service_account_file("path/to/credentials.json")
# index_client = MatchingEngineIndex(
#     credentials=creds,
#     index_name="projects/YOUR_PROJECT/locations/YOUR_LOCATION/indexes/YOUR_INDEX_ID"
# )
# index_client.upsert_datapoints(datapoints=dps)
# print("✅ Batch upsert completato!")
#
#
# new_index = index_client.upsert_datapoints(datapoints=dps)
