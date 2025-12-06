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