# small-rag  
A lightweight, dependency-free Retrieval-Augmented Generation (RAG) engine for Python.

**small-rag** is a minimal, easy-to-understand vector store + RAG toolkit.  
It is designed for developers who want a **simple, transparent, hackable RAG library** that can be fully understood in minutes.

No FAISS, no Qdrant, no heavy dependencies — just pure Python + SQLite.

---

## Features

- Pure Python implementation (no external dependencies)
- SQLite-backed vector store
- Pluggable embedding function (OpenAI, HF models, local LLMs, custom functions)
- Text preprocessing + chunking
- Metadata filtering
- Import/export database to JSON
- Command-line interface (`smallrag-cli`)
- Easy to read, extend, and embed inside other projects

---

## Installation

```bash
pip install small-rag
```

Verify:

```bash
python -m smallrag --help
```

---

## Quick Start (Python)

### 1. Create a RAG instance

```python
from smallrag import SmallRAG

rag = SmallRAG("my.db")
```

### 2. Set an embedder (required)

```python
rag.set_embedder(lambda t: [float(ord(c) % 255) for c in t[:64]])
```

### 3. Add documents

```python
rag.add_document("Python is a programming language created by Guido van Rossum.")
rag.add_document("Retrieval augmented generation improves LLM accuracy.")
```

### 4. Query

```python
res = rag.query("What is RAG?")
print(res)
```

Example output:

```json
[
  {
    "id": 2,
    "text": "retrieval augmented generation improves llm accuracy.",
    "metadata": {},
    "score": 0.87
  }
]
```

---

## Realistic Example (HuggingFace Embeddings)

```python
from smallrag import SmallRAG
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
rag = SmallRAG("docs.db")

rag.set_embedder(lambda t: model.encode(t).tolist())

rag.add_document("Paris is the capital of France.", metadata={"topic": "geography"})
rag.add_document("The Eiffel Tower is in Paris.", metadata={"topic": "landmark"})

print(rag.query("Where is the Eiffel Tower?"))
```
### OR 
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def st_embed(text: str):
    return model.encode(text).tolist()

rag = SmallRAG('data/rag.db')
rag.set_embedder(st_embed)
rag.add_document('Example doc about kafka and streaming')
print(rag.query('kafka streaming'))

# Export/Import
rag.export_db('backup.json')
rag.import_db('backup.json')
```
---

## CLI Usage

### Add a document

```bash
smallrag-cli --db my.db add "Python is easy to learn"
```

With metadata:

```bash
smallrag-cli --db my.db add "Paris is beautiful" --meta '{"country": "France"}'
```

### Query

```bash
smallrag-cli --db my.db query "What is Python?"
```

### Export DB

```bash
smallrag-cli --db my.db export dump.json
```

### Import DB

```bash
smallrag-cli --db my.db import dump.json
```

---

## Filtering by Metadata

```python
rag.query("Paris", filter={"country": "France"})
```

---

## Chunking Behavior

Default:

- chunk size: 512
- overlap: 64

```python
rag.add_document(big_text, chunk=True, chunk_size=256)
```

---

## Using OpenAI Embeddings

```python
from smallrag import SmallRAG
from openai import OpenAI

client = OpenAI()

rag = SmallRAG("openai.db")

def openai_embed(t: str):
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=t
    )
    return emb.data[0].embedding

rag.set_embedder(openai_embed)
rag.add_document("The Amazon rainforest is the largest rainforest on Earth.")

print(rag.query("What is the largest rainforest?"))
```

---

## Contributing

Pull requests welcome.  
If you use small-rag, share feedback via issues.

---

## License

MIT License.
