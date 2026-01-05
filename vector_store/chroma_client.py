# vector_store/chroma_client.py

import chromadb
from typing import Optional
from config.settings import CHROMA_PERSIST_DIR


class ChromaClient:
    """
    Manages ChromaDB client and collections.
    Supports one collection per hackathon.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PERSIST_DIR)
        )

    def get_collection(self, hackathon_id: str):
        """
        Get or create a collection for a hackathon.

        Args:
            hackathon_id: unique hackathon identifier
        """
        collection_name = f"hackathon_{hackathon_id}"

        return self.client.get_or_create_collection(
            name=collection_name
        )

    def persist(self):
        """
        Persist data to disk.
        Note: PersistentClient automatically persists, but we keep this for compatibility.
        """
        pass
