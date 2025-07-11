# Document Augmentation RAG Application (autogenerated)

This application implements an enhanced Retrieval-Augmented Generation (RAG) approach using document augmentation via question generation. The overall pipeline involves:

- **Document Processing:** Extracting text from PDF files, chunking the text, and generating questions from each chunk.
- **Embedding Generation & Vector Store:** Creating embeddings for both text chunks and generated questions, and storing them in a vector database.
- **Semantic Search & Response Generation:** Performing semantic search over the vector store, preparing the context, and generating responses using a language model.
- **Evaluation:** Optionally evaluating the generated response against a reference answer.

## Folder structure
Il repository è organizzato secondo la seguente struttura:

    .
    ├── app_evaluate.py            # Entry point for generating augmented responses and evaluating them
    ├── app_rag_pipeline.py        # Entry point for processing documents and building the vector store
    │
    ├── document_rag_agents/       # Core agents and pipelines for the application
    │   ├── base_agents/           # Low-level agents for specific tasks
    │   │   ├── chat_agent.py      # Handles LLM-based chat and response generation
    │   │   ├── docai_agent.py     # (Optional) Additional document AI functions
    │   │   ├── embedding_agent.py # Embedding generation functionalities
    │   │   └── text_chunker.py    # Text chunking functions
    │   │
    │   ├── complex_agents/        # High-level agents that combine base agents
    │   │   ├── rag_pipeline.py            # Pipeline to process document (extract, chunk, question generation, vector store)
    │   │   ├── semantic_search_agent.py   # Semantic search functionalities using vector embeddings
    │   │   └── vector_search_agent.py     # Combines search and context preparation
    │   │
    │   ├── db/                   # Database / storage modules
    │   │   ├── query_data.py      # Handles query and reference data extraction from JSON files
    │   │   └── simple_vector_store.py  # A simple vector store using NumPy
    │   │
    │   └── pipelines/            # Orchestrators for complete workflows
    │       ├── generate_augmented_response.py  # Generates augmented responses with optional evaluation
    │       └── generate_pipeline_v2.py           # Alternative pipeline for generating and evaluating responses
    │
    └── data/                     # Sample data folder
        ├── AI_information.pdf    # PDF file containing the document to process
        └── val.json              # JSON file containing query and ideal answer for evaluation 

## Getting Started

### Prerequisites

- Python 3.7+
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) (`pip install pymupdf`)
- [NumPy](https://numpy.org/) (`pip install numpy`)
- [tqdm](https://tqdm.github.io/) (`pip install tqdm`)
- OpenAI Python Client (ensure you have access to the API key)
- Environment variable `OPENAI_API_KEY` set with your API key

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/document-augmentation-rag.git
   cd document-augmentation-rag
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key:**

   Ensure that your `OPENAI_API_KEY` is set in your environment:

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

### Running the Application

#### 1. Process a Document

Run the RAG pipeline to extract text, generate chunks, augment them with questions, and build the vector store:

```bash
python app_rag_pipeline.py
```

This script processes the PDF file `data/AI_information.pdf` and prints:
- The number of items in the vector store.
- The number of text chunks created.
- The first text chunk for preview.

#### 2. Generate Augmented Response & Evaluation

Run the evaluation pipeline to generate an augmented response from the processed document and optionally evaluate it:

```bash
python app_evaluate.py
```

This script uses the pipeline defined in `document_rag_agents/pipelines/generate_augmented_response.py` to:
- Retrieve the query and reference data from `data/val.json`.
- Perform semantic search over the vector store.
- Generate and print the response.
- Optionally evaluate the response and print the evaluation results.

## Modules Overview

### Base Agents

- **chat_agent.py:** Handles LLM-based chat generation and evaluation.
- **docai_agent.py:** (Optional) Contains additional document processing functionalities.
- **embedding_agent.py:** Manages embedding creation using OpenAI's embedding API.
- **text_chunker.py:** Provides text chunking functionality.

### Complex Agents

- **rag_pipeline.py:** Orchestrates the complete document processing pipeline.
- **semantic_search_agent.py:** Performs semantic search using cosine similarity.
- **vector_search_agent.py:** Combines semantic search with context preparation for generating responses.

### Database (DB)

- **query_data.py:** Retrieves query data and reference answers from JSON files.
- **simple_vector_store.py:** Implements a simple vector store using NumPy arrays.

### Pipelines

- **generate_augmented_response.py:** High-level pipeline that generates augmented responses and optionally evaluates them.
- **generate_pipeline_v2.py:** Alternative generation pipeline with integrated response evaluation.

## IA e Ragionamento Giuridico

### Ricerca neuro-simbolica per il ragionamento giuridico complesso

Per costruire un agente di ragionamento giuridico (complesso) il miglior candidato sembra riguardare le intelligenze artificiali neuro-simboliche.


- https://github.com/IBM/neuro-symbolic-ai
- https://ibm.github.io/neuro-symbolic-ai/
- https://github.com/IBM/LNN

---

## ✅ Soluzioni commerciali di successo

### • **Westlaw Precision (Thomson Reuters)**

Utilizza LLM ottimizzati su giurisprudenza e normativa locale, integrati con il loro database legale, per rispondere a domande giuridiche in modo affidabile e citare fonti ufficiali .

### • **Bench IQ**

Startup che analizza pattern decisionali dei giudici, non solo statistiche, per aiutare avvocati a costruire argomentazioni mirate ([reuters.com][1]).

### • **Harvey (Counsel AI)**

Basato su GPT‑4, offre LLM specializzati per studi legali, integrando motori personalizzati pensati per il workflow giuridico .

### • **Hebbia Matrix**

Piattaforma per query semantiche in linguaggio naturale su contratti e documenti legali, con citazioni automatiche delle fonti ([en.wikipedia.org][2]).

---

## ⚙️ Tecnologie & approcci avanzati usati negli ambiti accademici e industriali

### 1. Architetture **neuro‑symboliche**

* **MRKL Systems** (AI21 Labs): sistema modulare che combina LLM con knowledge graph e ragionamento discreto ([arxiv.org][3]).
* **Logical Neural Networks** (IBM): neuroni legati a formule logiche, con inferenza interpretabile e differenziabile ([github.com][4]).
* Varie librerie:

  * **Logic Tensor Networks**, **DeepProbLog**, **Scallop**, **TensorLog**, **Markov Logic Networks** – tutte volte a integrare logica simbolica con deep learning ([github.com][5]).

### 2. Knowledge Graph & Retrieval‑Augmented Generation (RAG)

* Sistemi che estraggono strutture simboliche da LLM e le arricchiscono mediante knowledge graph, chiudendo il ciclo tra generazione e verifica simbolica .
* Applicazioni pratiche: contratti, contabilità, document compliance.

### 3. Progetti accademici rilevanti

* **NS‑LCR**: framework neuro‑symbolico per ranking di sentenze con spiegazioni logiche ([en.wikipedia.org][2], [arxiv.org][6]).
* **Logical LLMs in Law**: integrazione di LLM aperti con ragionamenti logici su contratti d’assicurazione, mostrando vantaggi di precisione e coerenza ([arxiv.org][7]).
* **NeSyGPT**: usa foundation models per estrarre simboli e generare programmi logici symbolic reasoning in modo scalabile ([axi.lims.ac.uk][8]).

---

## 🛠️ Tecnologie principali usate

| Tecnologia                         | Scopo                                      | Esempi                                |
| ---------------------------------- | ------------------------------------------ | ------------------------------------- |
| **LLM adattati al settore legale** | Comprensione del linguaggio giuridico      | Thomson Reuters, Harvey               |
| **Knowledge Graph**                | Struttura semantica e relazionale          | AllegroGraph, IBM toolkit             |
| **Motori simbolici**               | Logica formale e inferenza                 | Prolog, Drools, Logic Tensor Networks |
| **Neuro‑symbolic frameworks**      | Integrazione tra apprendimento e logica    | MRKL, DeepProbLog, Scallop            |
| **RAG/Graph-RAG**                  | Recupero dinamico di conoscenza affidabile | pipeline di ricerca espansa           |

---

## 🧭 Perché questi approcci funzionano

1. **Affidabilità**: le LLM garantiscono qualità linguistica, i motori simbolici danno coerenza e spiegabilità.
2. **Scalabilità**: Knowledge Graph + RAG riduce errori come le “hallucination”.
3. **Spiegazione**: i logici simbolici assicurano trasparenza, cruciale in ambito legale.

---

### 🔎 Conclusione

I migliori risultati nel ragionamento giuridico automatizzato si ottengono combinando:

* LLM specifici per ambito legale,
* Knowledge Graph ricchi di strutture simboliche,
* Motori formali per inferenza,
* Pipeline RAG per garantire accuratezza nelle citazioni e aggiornamento delle fonti.

Un approccio **neuro‑symbolico**, integrato e iterativo, appare oggi la strada più promettente per bilanciare **flessibilità**, **coerenza** e **spiegabilità**.

Se vuoi, posso approfondire uno di questi temi o mostrarti demo/liberie specifiche.

[1]: https://www.reuters.com/legal/transactional/new-legal-ai-venture-promises-show-how-judges-think-2024-02-29/?utm_source=chatgpt.com "New legal AI venture promises to show how judges think"
[2]: https://en.wikipedia.org/wiki/Hebbia?utm_source=chatgpt.com "Hebbia"
[3]: https://arxiv.org/abs/2205.00445?utm_source=chatgpt.com "MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning"
[4]: https://github.com/IBM/neuro-symbolic-ai?utm_source=chatgpt.com "GitHub - IBM/neuro-symbolic-ai: Neuro-Symbolic AI Toolkit"
[5]: https://github.com/mattfaltyn/awesome-neuro-symbolic-ai?utm_source=chatgpt.com "GitHub - mattfaltyn/awesome-neuro-symbolic-ai: A curated list of awesome Neuro-Symbolic AI frameworks, libraries, software, papers, and videos."
[6]: https://arxiv.org/abs/2403.01457?utm_source=chatgpt.com "Logic Rules as Explanations for Legal Case Retrieval"
[7]: https://arxiv.org/abs/2502.17638?utm_source=chatgpt.com "Towards Robust Legal Reasoning: Harnessing Logical LLMs in Law"
[8]: https://axi.lims.ac.uk/paper/2402.01889?utm_source=chatgpt.com "The Role of Foundation Models in Neuro-S..."



### Ricerca


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License.

---

*Enjoy building your document augmentation RAG system and happy coding!*
```
