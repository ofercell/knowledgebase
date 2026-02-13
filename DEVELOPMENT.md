# Knowledge Base System - Developer Documentation

## Architecture Overview

### Components

1. **Document Processors** (`src/knowledgebase/processors/`)
   - `base.py`: Abstract base class for all processors
   - `pdf_processor.py`: PDF document processing
   - `docx_processor.py`: DOCX document processing
   - `__init__.py`: Factory for creating appropriate processors

2. **Storage Layer** (`src/knowledgebase/storage/`)
   - `knowledge_store.py`: Vector database interface using ChromaDB
   - Handles embedding generation and similarity search

3. **QA System** (`src/knowledgebase/qa/`)
   - `qa_system.py`: Question answering and insights extraction
   - Uses LangChain and OpenAI for natural language processing

4. **Main Interface** (`src/knowledgebase/`)
   - `knowledge_base.py`: High-level API for the system
   - `config.py`: Configuration management

5. **CLI** (`src/kb_cli.py`)
   - Command-line interface for all operations

### Data Flow

```
Document File → Processor → Chunks → Embeddings → ChromaDB
                                                      ↓
User Question → Embedding → Similarity Search → Context → LLM → Answer
```

## Adding New Features

### Adding a New Document Processor

1. Create a new processor class in `src/knowledgebase/processors/`:

```python
from pathlib import Path
from typing import List
from .base import DocumentProcessor, DocumentChunk

class MyProcessor(DocumentProcessor):
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == '.myformat'
    
    def process(self, file_path: Path) -> List[DocumentChunk]:
        # Your processing logic
        chunks = []
        # ... extract content ...
        return chunks
```

2. Register it in `processors/__init__.py`:

```python
from .my_processor import MyProcessor

class DocumentProcessorFactory:
    def __init__(self):
        self.processors = []
        # ... existing processors ...
        try:
            self.processors.append(MyProcessor())
        except ImportError:
            pass
```

### Adding New QA Capabilities

Extend the `QASystem` class in `src/knowledgebase/qa/qa_system.py`:

```python
def my_new_feature(self, document_name: Optional[str] = None):
    """Add new feature."""
    search_results = self.knowledge_store.search(
        query="relevant query",
        n_results=5
    )
    # Process results...
    return results
```

### Customizing Embeddings

Modify `src/knowledgebase/storage/knowledge_store.py`:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

# In __init__:
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```

## Configuration

### Environment Variables

All configuration is in `src/knowledgebase/config.py`:

- `OPENAI_API_KEY`: OpenAI API key (required)
- `OPENAI_MODEL`: Model for QA (default: gpt-4)
- `EMBEDDING_MODEL`: Model for embeddings (default: text-embedding-3-small)
- `CHROMA_DB_PATH`: Database path (default: ./data/chromadb)
- `DOCUMENTS_PATH`: Document storage (default: ./data/documents)
- `CHUNK_SIZE`: Text chunk size (default: 1000)
- `CHUNK_OVERLAP`: Chunk overlap (default: 200)

### Chunking Strategy

Modify `config.py`:

```python
CHUNK_SIZE = 500  # Smaller chunks
CHUNK_OVERLAP = 100  # Less overlap
```

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=src/knowledgebase tests/
```

### Writing Tests

Create test files in `tests/`:

```python
import pytest
from knowledgebase.knowledge_base import KnowledgeBase

def test_add_document():
    kb = KnowledgeBase()
    result = kb.add_document("test.pdf")
    assert result['chunks_added'] > 0
```

## Performance Optimization

### Batch Processing

Process multiple documents:

```python
kb = KnowledgeBase()
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

for doc in documents:
    print(f"Processing {doc}...")
    kb.add_document(doc)
```

### Caching

ChromaDB automatically handles caching. For additional caching:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str):
    return kb.ask_question(query)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Verify `.env` file:
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

3. **ChromaDB Errors**: Clear database:
   ```bash
   rm -rf data/chromadb
   ```

4. **Hebrew Text Issues**: Ensure UTF-8 encoding:
   ```python
   # In your code
   with open(file, 'r', encoding='utf-8') as f:
       content = f.read()
   ```

## Best Practices

1. **Document Naming**: Use descriptive, unique names
2. **Error Handling**: Always wrap operations in try-except
3. **Validation**: Validate inputs before processing
4. **Logging**: Add logging for debugging
5. **Testing**: Write tests for new features
6. **Documentation**: Update docs when changing APIs

## Extending the System

### Adding New Commands

Edit `src/kb_cli.py`:

```python
# Add subparser
new_parser = subparsers.add_parser("newcmd", help="New command")
new_parser.add_argument("arg", help="Argument")

# Add handler
elif args.command == "newcmd":
    result = kb.new_feature(args.arg)
    print(result)
```

### Custom Prompts

Modify prompts in `src/knowledgebase/qa/qa_system.py`:

```python
self.system_prompt = """Your custom prompt here
With instructions...
"""
```

## API Reference

See Python docstrings in each module for detailed API documentation.

### Main Classes

- `KnowledgeBase`: Main interface
- `DocumentProcessor`: Base for processors
- `KnowledgeStore`: Vector storage
- `QASystem`: Question answering
