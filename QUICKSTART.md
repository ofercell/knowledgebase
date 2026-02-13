# Quick Start Guide

## Installation

1. **Clone and Install**
```bash
git clone https://github.com/ofercell/knowledgebase.git
cd knowledgebase
pip install -r requirements.txt
```

2. **Configure**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

3. **Test Installation**
```bash
python src/kb_cli.py --help
```

## First Steps

### 1. Add Your First Document

```bash
# Add the sample document
python src/kb_cli.py add examples/sample_functional_spec.md

# You should see:
# Processing document: sample_functional_spec.md
# Extracted X chunks from document
# Adding to knowledge store...
# ✓ Document added successfully!
```

### 2. Ask a Question

```bash
python src/kb_cli.py ask "What are the user stories?"

# You should get an answer based on the document content
```

### 3. Extract Insights

```bash
python src/kb_cli.py insights

# You should see a list of key insights from the document
```

### 4. Generate Tests

```bash
python src/kb_cli.py generate-tests --type functional

# You should see generated test cases
```

## Common Workflows

### Daily Usage

```bash
# Check what's in the knowledge base
python src/kb_cli.py list

# Get statistics
python src/kb_cli.py stats

# Ask questions as needed
python src/kb_cli.py ask "Your question here"
```

### Adding Multiple Documents

```bash
# Create a docs folder
mkdir -p my_docs

# Add all documents
for file in my_docs/*; do
    python src/kb_cli.py add "$file"
done

# Verify
python src/kb_cli.py list
```

### Research Session

```bash
# Extract all insights
python src/kb_cli.py insights --max 20 > project_insights.txt

# Generate test plan
python src/kb_cli.py generate-tests > test_plan.txt

# Ask specific questions
python src/kb_cli.py ask "What are the security requirements?"
python src/kb_cli.py ask "How should authentication work?"
python src/kb_cli.py ask "What are the performance targets?"
```

## Tips for Best Results

1. **Document Quality**: Use well-structured documents with clear sections
2. **Specific Questions**: Ask specific questions for better answers
3. **Context Size**: Increase --results for complex questions
4. **Regular Updates**: Re-add documents when they change
5. **Naming**: Use descriptive filenames

## Troubleshooting

### "OPENAI_API_KEY is not set"
- Make sure your .env file exists and has the API key
- Alternatively, export it: `export OPENAI_API_KEY=your-key`

### "No processor found for file type"
- Check the file extension (.pdf or .docx)
- Verify the file is not corrupted

### "Error processing document"
- Ensure the document is valid and not password-protected
- Check file permissions

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed examples
- See [DEVELOPMENT.md](DEVELOPMENT.md) for customization
- Add your real project documents
- Integrate with your workflow

## Support

For issues or questions:
- Open an issue on GitHub
- Check documentation
- Review examples

Enjoy using the Knowledge Base System!
