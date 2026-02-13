"""Base document processor interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """Represents a chunk of document content with metadata."""
    
    content: str
    metadata: Dict[str, Any]
    page_number: int = None
    chunk_index: int = None


class DocumentProcessor(ABC):
    """Abstract base class for document processors."""
    
    @abstractmethod
    def can_process(self, file_path: Path) -> bool:
        """Check if this processor can handle the given file."""
        pass
    
    @abstractmethod
    def process(self, file_path: Path) -> List[DocumentChunk]:
        """
        Process a document and return chunks of content.
        
        Args:
            file_path: Path to the document to process
            
        Returns:
            List of DocumentChunk objects containing content and metadata
        """
        pass
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract basic metadata from file."""
        return {
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_extension": file_path.suffix,
        }
