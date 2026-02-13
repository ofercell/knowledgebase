"""Main Knowledge Base Manager."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil

from .config import config
from .processors import DocumentProcessorFactory
from .storage import KnowledgeStore
from .qa import QASystem


class KnowledgeBase:
    """Main interface for the knowledge base system."""
    
    def __init__(self):
        """Initialize the knowledge base."""
        # Validate configuration
        config.validate()
        config.ensure_directories()
        
        # Initialize components
        self.processor_factory = DocumentProcessorFactory()
        self.knowledge_store = KnowledgeStore()
        self.qa_system = QASystem(self.knowledge_store)
    
    def add_document(self, file_path: str) -> Dict[str, Any]:
        """
        Add a document to the knowledge base.
        
        Args:
            file_path: Path to the document to add
            
        Returns:
            Dictionary with processing results
        """
        file_path = Path(file_path)
        
        # Process the document
        print(f"Processing document: {file_path.name}")
        chunks = self.processor_factory.process_document(file_path)
        
        print(f"Extracted {len(chunks)} chunks from document")
        
        # Add to knowledge store
        print("Adding to knowledge store...")
        chunk_ids = self.knowledge_store.add_document_chunks(chunks)
        
        # Copy document to storage
        dest_path = Path(config.DOCUMENTS_PATH) / file_path.name
        shutil.copy2(file_path, dest_path)
        
        print(f"Successfully added document: {file_path.name}")
        
        return {
            "filename": file_path.name,
            "chunks_added": len(chunk_ids),
            "stored_path": str(dest_path)
        }
    
    def ask_question(self, question: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Ask a question about the documents in the knowledge base.
        
        Args:
            question: The question to ask
            n_results: Number of context documents to use
            
        Returns:
            Dictionary with answer and sources
        """
        return self.qa_system.answer_question(question, n_results)
    
    def get_insights(
        self,
        document_name: Optional[str] = None,
        max_insights: int = 10
    ) -> List[str]:
        """
        Extract insights from documents.
        
        Args:
            document_name: Optional specific document
            max_insights: Maximum number of insights
            
        Returns:
            List of insights
        """
        return self.qa_system.extract_insights(document_name, max_insights)
    
    def generate_tests(
        self,
        document_name: Optional[str] = None,
        test_type: str = "functional"
    ) -> List[Dict[str, str]]:
        """
        Generate test cases from documentation.
        
        Args:
            document_name: Optional specific document
            test_type: Type of tests (functional, integration, unit)
            
        Returns:
            List of test cases
        """
        return self.qa_system.generate_tests(document_name, test_type)
    
    def list_documents(self) -> List[str]:
        """
        List all documents in the knowledge base.
        
        Returns:
            List of document names
        """
        return self.knowledge_store.get_all_documents()
    
    def delete_document(self, filename: str) -> Dict[str, Any]:
        """
        Delete a document from the knowledge base.
        
        Args:
            filename: Name of document to delete
            
        Returns:
            Dictionary with deletion results
        """
        chunks_deleted = self.knowledge_store.delete_document(filename)
        
        # Delete physical file if exists
        file_path = Path(config.DOCUMENTS_PATH) / filename
        if file_path.exists():
            file_path.unlink()
            file_deleted = True
        else:
            file_deleted = False
        
        return {
            "filename": filename,
            "chunks_deleted": chunks_deleted,
            "file_deleted": file_deleted
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base.
        
        Returns:
            Dictionary with statistics
        """
        return self.knowledge_store.get_stats()
