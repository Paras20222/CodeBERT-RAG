class VectorStore:
    def __init__(self, dimension: int = 768, index_type: str = "hnsw"):
        self.dimension = dimension
        self.index_type = index_type
        self.index = self._create_index()
        self.documents = []
        self.id_to_index = {}

    def _create_index(self) -> faiss.Index:
        if self.index_type == "flat":
            return faiss.IndexFlatIP(self.dimension)
        elif self.index_type == "hnsw":
            index = faiss.IndexHNSWFlat(self.dimension, 32)
            index.hnsw.efConstruction = 64
            index.hnsw.efSearch = 32
            return index
        elif self.index_type == "ivf":
            nlist = 100
            quantizer = faiss.IndexFlatL2(self.dimension)
            index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            index.nprobe = 10
            return index
        raise ValueError(f"Unsupported index type: {self.index_type}")

    def add_documents(self, documents: List[Document], embeddings: Optional[np.ndarray] = None):
        if embeddings is not None:
            assert len(documents) == embeddings.shape[0]
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings)
        start_idx = len(self.documents)
        for i, doc in enumerate(documents):
            self.id_to_index[doc.id] = start_idx + i
            if embeddings is not None:
                doc.embedding = embeddings[i]
            self.documents.append(doc)

    def search(self, query_embedding: np.ndarray, k: int = 5, filter_fn: Optional[callable] = None) -> List[Tuple[Document, float]]:
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, k * 2)
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1:
                doc = self.documents[idx]
                if filter_fn is None or filter_fn(doc):
                    results.append((doc, float(distance)))
                    if len(results) == k:
                        break
        return results[:k]
