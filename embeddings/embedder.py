# embeddings/embedder.py

from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
import threading


class EmbeddingGenerator:

    _model = None
    _lock = threading.Lock()

    def __init__(self, model_name: str):
        self.model_name = model_name
        self._load_model()

    def _load_model(self):
        """
        Load the embedding model exactly once.
        """
        if EmbeddingGenerator._model is None:
            with EmbeddingGenerator._lock:
                if EmbeddingGenerator._model is None:
                    EmbeddingGenerator._model = SentenceTransformer(
                        self.model_name
                    )

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of raw chunk texts

        Returns:
            numpy.ndarray of shape (len(texts), embedding_dim)
        """

        if not texts:
            raise ValueError("No texts provided for embedding")

        embeddings = EmbeddingGenerator._model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings

    def embed_chunks(self, chunks: List) -> List[Dict]:
        """
        Generate embeddings for Chunk objects.

        Each output item contains:
        - embedding
        - original text
        - metadata

        Args:
            chunks: List of Chunk objects

        Returns:
            List of dicts ready for vector storage
        """

        texts = [chunk.text for chunk in chunks]

        embeddings = self.embed_texts(texts)

        embedded_chunks = []

        for idx, chunk in enumerate(chunks):
            embedded_chunks.append({
                "embedding": embeddings[idx],
                "text": chunk.text,
                "metadata": chunk.metadata
            })

        return embedded_chunks
