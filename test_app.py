from smallrag import SmallRAG

def embed(text):
    # simple deterministic char-based embedding
    return [float(ord(c) % 255) for c in text[:64]]

rag = SmallRAG("test.db", verbose=True)
rag.set_embedder(embed)

rag.add_document("Kafka is a distributed streaming platform.")
rag.add_document("Spark is used for big data processing.")

results = rag.query("stream processing")
print(results)