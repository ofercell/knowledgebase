"""Tests for the Knowledge Base system."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from knowledgebase.processors.base import DocumentChunk
from knowledgebase.processors import DocumentProcessorFactory


class TestDocumentProcessorFactory:
    """Tests for DocumentProcessorFactory."""
    
    def test_factory_initialization(self):
        """Test that factory initializes with processors."""
        factory = DocumentProcessorFactory()
        assert len(factory.processors) > 0
    
    def test_get_processor_for_pdf(self):
        """Test getting PDF processor."""
        factory = DocumentProcessorFactory()
        pdf_path = Path("test.pdf")
        processor = factory.get_processor(pdf_path)
        assert processor is not None
    
    def test_get_processor_for_docx(self):
        """Test getting DOCX processor."""
        factory = DocumentProcessorFactory()
        docx_path = Path("test.docx")
        processor = factory.get_processor(docx_path)
        assert processor is not None
    
    def test_get_processor_for_unknown(self):
        """Test getting processor for unknown format."""
        factory = DocumentProcessorFactory()
        unknown_path = Path("test.xyz")
        processor = factory.get_processor(unknown_path)
        assert processor is None
    
    def test_process_document_not_found(self):
        """Test processing non-existent document."""
        factory = DocumentProcessorFactory()
        with pytest.raises(FileNotFoundError):
            factory.process_document(Path("nonexistent.pdf"))


class TestDocumentChunk:
    """Tests for DocumentChunk."""
    
    def test_document_chunk_creation(self):
        """Test creating a DocumentChunk."""
        chunk = DocumentChunk(
            content="Test content",
            metadata={"filename": "test.pdf"},
            page_number=1,
            chunk_index=0
        )
        assert chunk.content == "Test content"
        assert chunk.metadata["filename"] == "test.pdf"
        assert chunk.page_number == 1
        assert chunk.chunk_index == 0


class TestConfiguration:
    """Tests for configuration."""
    
    def test_config_import(self):
        """Test that config can be imported."""
        from knowledgebase.config import config
        assert config is not None
    
    def test_config_validation_with_key(self):
        """Test config validation with API key."""
        from knowledgebase.config import Config
        # Create a fresh config instance with the test key
        old_key = Config.OPENAI_API_KEY
        Config.OPENAI_API_KEY = 'test-key'
        try:
            Config.validate()
        except ValueError:
            pytest.fail("Config validation should pass with API key")
        finally:
            Config.OPENAI_API_KEY = old_key
    
    @patch.dict('os.environ', {}, clear=True)
    def test_config_validation_without_key(self):
        """Test config validation without API key."""
        from knowledgebase.config import Config
        config = Config()
        config.OPENAI_API_KEY = ""
        with pytest.raises(ValueError):
            config.validate()


# Integration tests would go here
# These would require actual files and API keys, so we mock them

class TestKnowledgeBaseIntegration:
    """Integration tests for KnowledgeBase (mocked)."""
    
    @patch('knowledgebase.knowledge_base.KnowledgeStore')
    @patch('knowledgebase.knowledge_base.QASystem')
    @patch('knowledgebase.config.config.validate')
    @patch('knowledgebase.config.config.ensure_directories')
    def test_knowledge_base_initialization(self, mock_dirs, mock_validate, mock_qa, mock_store):
        """Test KnowledgeBase initialization."""
        from knowledgebase.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase()
        assert kb is not None
        mock_validate.assert_called_once()
        mock_dirs.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
