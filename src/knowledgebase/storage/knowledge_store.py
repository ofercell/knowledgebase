"""Vector storage for knowledge base using ChromaDB."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

from langchain_openai import OpenAIEmbeddings

from ..config import config
from ..processors.base import DocumentChunk


class KnowledgeStore:
    """Store and retrieve document knowledge using vector embeddings."""
    
    def __init__(self, collection_name: str = "knowledge_base"):
        """
        Initialize the knowledge store.
        
        Args:
            collection_name: Name of the ChromaDB collection
        """
        if chromadb is None:
            raise ImportError(
                "chromadb is required. Install it with: pip install chromadb"
            )
        
        config.ensure_directories()
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_PATH
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Knowledge base for process documents"}
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
    
    def add_document_chunks(self, chunks: List[DocumentChunk]) -> List[str]:
        """
        Add document chunks to the knowledge store.
        
        Args:
            chunks: List of DocumentChunk objects to add
            
        Returns:
            List of IDs for the added chunks
        """
        if not chunks:
            return []
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        
        for chunk in chunks:
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            documents.append(chunk.content)
            
            # Prepare metadata (ChromaDB requires simple types)
            metadata = {
                "filename": chunk.metadata.get("filename", ""),
                "file_path": chunk.metadata.get("file_path", ""),
                "file_extension": chunk.metadata.get("file_extension", ""),
                "chunk_type": chunk.metadata.get("chunk_type", "text"),
            }
            
            if chunk.page_number:
                metadata["page_number"] = chunk.page_number
            if chunk.chunk_index is not None:
                metadata["chunk_index"] = chunk.chunk_index
            
            metadatas.append(metadata)
        
        # Generate embeddings
        embeddings_list = self.embeddings.embed_documents(documents)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings_list,
            metadatas=metadatas
        )
        
        return ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of search results with content and metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        
        if results and results["documents"]:
            for i in range(len(results["documents"][0])):
                result = {
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_all_documents(self) -> List[str]:
        """
        Get list of all unique documents in the store.
        
        Returns:
            List of document filenames
        """
        # Get all items from collection
        results = self.collection.get()
        
        if not results or not results.get("metadatas"):
            return []
        
        # Extract unique filenames
        filenames = set()
        for metadata in results["metadatas"]:
            if "filename" in metadata:
                filenames.add(metadata["filename"])
        
        return sorted(list(filenames))
    
    def delete_document(self, filename: str) -> int:
        """
        Delete all chunks related to a document.
        
        Args:
            filename: Name of the document to delete
            
        Returns:
            Number of chunks deleted
        """
        # Get all chunks for this document
        results = self.collection.get(
            where={"filename": filename}
        )
        
        if not results or not results.get("ids"):
            return 0
        
        # Delete chunks
        self.collection.delete(ids=results["ids"])
        
        return len(results["ids"])
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge store.
        
        Returns:
            Dictionary with statistics
        """
        count = self.collection.count()
        documents = self.get_all_documents()
        
        return {
            "total_chunks": count,
            "total_documents": len(documents),
            "documents": documents
        }
