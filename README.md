# Knowledge Base System

A comprehensive knowledge base system for processing and analyzing process documents including functional specifications, technical specifications, and working instructions. Supports documents with Hebrew text and images.

## Features

- **Document Processing**: Support for PDF and DOCX files with Hebrew text and images
- **Deep Insights Extraction**: Automatically extract key insights from documents
- **Question Answering**: Ask questions about your documents and get accurate answers
- **Test Generation**: Generate functional, integration, and unit tests from documentation
- **Vector Storage**: Efficient storage and retrieval using ChromaDB
- **Multi-language Support**: Works with Hebrew and English text

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ofercell/knowledgebase.git
cd knowledgebase
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Quick Start

### Adding Documents

Add a document to the knowledge base:
```bash
python src/kb_cli.py add path/to/your/document.pdf
```

Supported formats:
- PDF files (`.pdf`)
- Word documents (`.docx`)

### Asking Questions

Ask questions about your documents:
```bash
python src/kb_cli.py ask "What are the main requirements?"
```

Questions can be in English or Hebrew.

### Extracting Insights

Extract key insights from all documents:
```bash
python src/kb_cli.py insights
```

Extract insights from a specific document:
```bash
python src/kb_cli.py insights --document myspec.pdf --max 15
```

### Generating Tests

Generate test cases from your documentation:
```bash
python src/kb_cli.py generate-tests --type functional
```

Test types:
- `functional` - Functional test cases
- `integration` - Integration test cases
- `unit` - Unit test cases

### Managing Documents

List all documents:
```bash
python src/kb_cli.py list
```

Show statistics:
```bash
python src/kb_cli.py stats
```

Delete a document:
```bash
python src/kb_cli.py delete document.pdf
```

## Python API

You can also use the knowledge base programmatically:

```python
from knowledgebase.knowledge_base import KnowledgeBase

# Initialize
kb = KnowledgeBase()

# Add a document
result = kb.add_document("path/to/document.pdf")

# Ask a question
answer = kb.ask_question("What is the authentication process?")
print(answer['answer'])

# Get insights
insights = kb.get_insights(max_insights=10)
for insight in insights:
    print(insight)

# Generate tests
tests = kb.generate_tests(test_type="functional")
for test in tests:
    print(test['full_text'])
```

## Architecture

The system consists of several modules:

- **Processors**: Handle different document formats (PDF, DOCX)
- **Storage**: Vector database for efficient document retrieval (ChromaDB)
- **QA System**: Question answering and insights extraction using LLM
- **CLI**: Command-line interface for easy interaction

## Configuration

Configuration is done via environment variables in `.env`:

```env
# Required
OPENAI_API_KEY=your_api_key_here

# Optional (with defaults)
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-3-small
CHROMA_DB_PATH=./data/chromadb
DOCUMENTS_PATH=./data/documents
```

## Hebrew Text Support

The system fully supports Hebrew text in documents:
- Hebrew text is properly extracted from PDF and DOCX files
- Questions can be asked in Hebrew
- Answers are provided in the same language as the question

## Requirements

- Python 3.8+
- OpenAI API key
- See `requirements.txt` for full list of dependencies

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
