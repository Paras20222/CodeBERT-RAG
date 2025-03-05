from typing import List, Dict, Tuple, Optional
import numpy as np
from dataclasses import dataclass
import faiss
import pickle

from .embeddings import CodeBERTEmbedder
from .vectorstore import VectorStore, Document

@dataclass
class RetrievedContext:
    """Enhanced context class with source tracking."""
    content: str
    metadata: Dict
    relevance_score: float
    source_type: str  # 'problem', 'editorial', or 'solution'
    confidence: float  # Confidence score for the retrieval

class RAGRetriever:
    def __init__(self, embedder: CodeBERTEmbedder, vector_store: VectorStore, max_context_length: int = 2000, min_confidence: float = 0.7):
        self.embedder = embedder
        self.vector_store = vector_store
        self.max_context_length = max_context_length
        self.min_confidence = min_confidence
        self.context_cache = {}

    def _process_query(self, query: str) -> Dict:
        query_info = {
            'type': self._detect_query_type(query),
            'difficulty': self._extract_difficulty(query),
            'topics': self._extract_topics(query),
            'embedding': self.embedder.generate_embedding(query)
        }
        return query_info

    def _detect_query_type(self, query: str) -> str:
        query = query.lower()
        if any(word in query for word in ['how', 'approach', 'solve']):
            return 'solution_request'
        if any(word in query for word in ['explain', 'understand', 'mean']):
            return 'explanation_request'
        if any(word in query for word in ['similar', 'like', 'related']):
            return 'similar_problems'
        return 'general'

    def _extract_difficulty(self, query: str) -> Optional[str]:
        difficulties = ['800', '1000', '1200', '1400', '1600', '1800', '2000']
        for diff in difficulties:
            if diff in query:
                return diff
        return None

    def _extract_topics(self, query: str) -> List[str]:
        topics = ['dp', 'graph', 'tree', 'string', 'math', 'greedy']
        return [topic for topic in topics if topic in query.lower()]

    def retrieve(self, query: str, k: int = 3) -> List[RetrievedContext]:
        query_info = self._process_query(query)
        filter_fn = lambda doc: self._filter_by_metadata(doc, query_info)
        results = self.vector_store.search(query_info['embedding'], k=k, filter_fn=filter_fn)
        
        contexts = []
        for doc, score in results:
            if score < self.min_confidence:
                continue
            source_type = doc.metadata.get('type', 'general')
            confidence = score * self._calculate_metadata_confidence(doc, query_info)
            context = RetrievedContext(
                content=doc.content[:self.max_context_length],
                metadata=doc.metadata,
                relevance_score=score,
                source_type=source_type,
                confidence=confidence
            )
            contexts.append(context)
            if score > 0.9:
                self.context_cache[doc.id] = context
        return contexts

    def _filter_by_metadata(self, doc: Document, query_info: Dict) -> bool:
        if query_info['difficulty'] and 'difficulty' in doc.metadata:
            if abs(int(doc.metadata['difficulty']) - int(query_info['difficulty'])) > 200:
                return False
        if query_info['topics'] and 'tags' in doc.metadata:
            if not any(topic in doc.metadata['tags'] for topic in query_info['topics']):
                return False
        return True

    def _calculate_metadata_confidence(self, doc: Document, query_info: Dict) -> float:
        confidence = 1.0
        if query_info['difficulty'] and 'difficulty' in doc.metadata:
            diff_delta = abs(int(doc.metadata['difficulty']) - int(query_info['difficulty']))
            confidence *= max(0.5, 1 - (diff_delta / 1000))
        if query_info['topics'] and 'tags' in doc.metadata:
            matching_topics = sum(1 for topic in query_info['topics'] if topic in doc.metadata['tags'])
            if matching_topics:
                confidence *= 1 + (0.1 * matching_topics)
        return min(1.0, confidence)
