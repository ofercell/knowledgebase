"""Document processor factory."""

from pathlib import Path
from typing import List, Optional

from .base import DocumentProcessor, DocumentChunk
from .pdf_processor import PDFProcessor
from .docx_processor import DOCXProcessor


class DocumentProcessorFactory:
    """Factory for creating appropriate document processors."""
    
    def __init__(self):
        """Initialize the factory with available processors."""
        self.processors = []
        
        # Register available processors
        try:
            self.processors.append(PDFProcessor())
        except ImportError:
            pass
        
        try:
            self.processors.append(DOCXProcessor())
        except ImportError:
            pass
    
    def get_processor(self, file_path: Path) -> Optional[DocumentProcessor]:
        """
        Get appropriate processor for the given file.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            DocumentProcessor instance or None if no processor found
        """
        for processor in self.processors:
            if processor.can_process(file_path):
                return processor
        return None
    
    def process_document(self, file_path: Path) -> List[DocumentChunk]:
        """
        Process a document using the appropriate processor.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of DocumentChunk objects
            
        Raises:
            ValueError: If no processor can handle the file
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        processor = self.get_processor(file_path)
        
        if processor is None:
            raise ValueError(
                f"No processor found for file type: {file_path.suffix}"
            )
        
        return processor.process(file_path)
