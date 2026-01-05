# vector_store/store.py

from typing import List, Dict, Any, Optional
import uuid


class VectorStore:
    """
    Handles add/search operations for a Chroma collection.
    """

    def __init__(self, collection):
        self.collection = collection

    def add_embeddings(self, embedded_chunks: List[Dict[str, Any]]):
        """
        Add embedded chunks to the vector store.

        Each embedded_chunk must contain:
        - embedding
        - text
        - metadata
        """

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for item in embedded_chunks:
            ids.append(str(uuid.uuid4()))
            documents.append(item["text"])
            embeddings.append(item["embedding"].tolist())
            metadatas.append(item["metadata"])

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def similarity_search(
        self,
        query_embedding,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search with optional metadata filters.
        """

        result = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=filters
        )
        

        retrieved = []

        for i in range(len(result["documents"][0])):
            retrieved.append({
                "text": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "distance": result["distances"][0][i]
            })

        return retrieved
