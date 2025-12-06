from smallrag import SmallRAG

def test_add_and_query(tmp_path):
    db = tmp_path / "test.db"
    rag = SmallRAG(str(db))

    # trivial embedder: unicode codepoints averaged
    def embed(s: str):
        if not s:
            return [0.0]
        arr = [ord(c) % 255 for c in s[:128]]
        # normalize
        norm = sum(arr) or 1
        return [x / norm for x in arr]

    rag.set_embedder(embed)
    rag.add_document("Kafka is a distributed streaming platform.")
    rag.add_document("Spark processes big data.")

    res = rag.query("stream processing", top_k=2)
    assert isinstance(res, list)
    assert len(res) <= 2
