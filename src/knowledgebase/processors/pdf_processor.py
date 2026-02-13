"""PDF document processor with image and text extraction."""

from pathlib import Path
from typing import List, Dict, Any
import io

try:
    import pypdf
except ImportError:
    try:
        import PyPDF2 as pypdf
    except ImportError:
        pypdf = None

try:
    from PIL import Image
except ImportError:
    Image = None

from .base import DocumentProcessor, DocumentChunk
from ..config import config


class PDFProcessor(DocumentProcessor):
    """Process PDF documents, extracting text and images."""
    
    def __init__(self):
        """Initialize PDF processor."""
        if pypdf is None:
            raise ImportError(
                "pypdf is required for PDF processing. "
                "Install it with: pip install pypdf"
            )
    
    def can_process(self, file_path: Path) -> bool:
        """Check if file is a PDF."""
        return file_path.suffix.lower() == '.pdf'
    
    def process(self, file_path: Path) -> List[DocumentChunk]:
        """
        Process PDF file and extract text content.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        metadata = self.extract_metadata(file_path)
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                metadata["num_pages"] = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    # Extract text from page
                    text = page.extract_text()
                    
                    if text.strip():
                        # Split text into chunks if needed
                        text_chunks = self._split_text(text)
                        
                        for idx, chunk_text in enumerate(text_chunks):
                            chunk = DocumentChunk(
                                content=chunk_text,
                                metadata={
                                    **metadata,
                                    "page_number": page_num,
                                    "chunk_type": "text"
                                },
                                page_number=page_num,
                                chunk_index=idx
                            )
                            chunks.append(chunk)
                
                # Note: Image extraction from PDF can be complex
                # This is a placeholder for future enhancement
                # Images would require additional processing with pytesseract
                
        except Exception as e:
            raise RuntimeError(f"Error processing PDF {file_path}: {str(e)}")
        
        return chunks
    
    def _split_text(self, text: str) -> List[str]:
        """
        Split text into chunks based on configuration.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        chunk_size = config.CHUNK_SIZE
        chunk_overlap = config.CHUNK_OVERLAP
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap
        
        return chunks
