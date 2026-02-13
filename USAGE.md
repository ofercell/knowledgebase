# Usage Examples

## Example 1: Processing a Functional Specification

```bash
# Add the functional specification
python src/kb_cli.py add examples/functional_spec.pdf

# Ask questions about it
python src/kb_cli.py ask "What are the user authentication requirements?"
python src/kb_cli.py ask "Which APIs need to be implemented?"

# Extract insights
python src/kb_cli.py insights --document functional_spec.pdf
```

## Example 2: Processing Multiple Documents

```bash
# Add multiple documents
python src/kb_cli.py add specs/functional_spec.docx
python src/kb_cli.py add specs/technical_spec.pdf
python src/kb_cli.py add instructions/deployment.docx

# Ask questions across all documents
python src/kb_cli.py ask "How should we deploy the system?"
python src/kb_cli.py ask "What are the database requirements?"

# View all documents
python src/kb_cli.py list
```

## Example 3: Test Generation

```bash
# Generate functional tests from documentation
python src/kb_cli.py generate-tests --type functional

# Generate tests from specific document
python src/kb_cli.py generate-tests --document functional_spec.pdf --type integration

# Generate unit tests
python src/kb_cli.py generate-tests --type unit
```

## Example 4: Hebrew Documents

```bash
# Add Hebrew documents
python src/kb_cli.py add docs/spec_hebrew.docx

# Ask in Hebrew
python src/kb_cli.py ask "מהן הדרישות העיקריות?"

# Extract insights
python src/kb_cli.py insights --document spec_hebrew.docx
```

## Example 5: Python API Usage

```python
from knowledgebase.knowledge_base import KnowledgeBase

# Initialize the knowledge base
kb = KnowledgeBase()

# Add documents
kb.add_document("functional_spec.pdf")
kb.add_document("technical_spec.docx")

# Get statistics
stats = kb.get_stats()
print(f"Total documents: {stats['total_documents']}")
print(f"Total chunks: {stats['total_chunks']}")

# Ask questions
qa_result = kb.ask_question("What are the security requirements?")
print(f"Answer: {qa_result['answer']}")
print(f"Sources: {qa_result['sources']}")

# Extract insights
insights = kb.get_insights(max_insights=5)
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

# Generate tests
tests = kb.generate_tests(test_type="functional")
for test in tests:
    print(test['full_text'])
    print("-" * 80)

# Clean up - delete a document
kb.delete_document("old_spec.pdf")
```

## Example 6: Advanced Queries

```bash
# Get more context for complex questions
python src/kb_cli.py ask "Explain the complete authentication flow" --results 10

# Extract many insights
python src/kb_cli.py insights --max 20

# Focus on specific document
python src/kb_cli.py ask "What testing is required?" 
# (will search all documents)
```

## Example 7: Workflow for New Project

```bash
# Step 1: Add all project documentation
python src/kb_cli.py add project/functional_spec.pdf
python src/kb_cli.py add project/technical_spec.docx
python src/kb_cli.py add project/architecture.pdf
python src/kb_cli.py add project/requirements.docx

# Step 2: Verify all documents are loaded
python src/kb_cli.py list
python src/kb_cli.py stats

# Step 3: Extract key insights
python src/kb_cli.py insights --max 20 > insights.txt

# Step 4: Generate test plan
python src/kb_cli.py generate-tests --type functional > test_plan.txt

# Step 5: Use Q&A during development
python src/kb_cli.py ask "How should error handling work?"
python src/kb_cli.py ask "What are the performance requirements?"
python src/kb_cli.py ask "Describe the database schema"
```

## Tips

1. **Document Organization**: Store documents in a dedicated folder before adding them
2. **Naming**: Use descriptive filenames as they appear in search results
3. **Context**: For better answers, include more context documents (--results parameter)
4. **Specificity**: Ask specific questions for better answers
5. **Regular Updates**: Re-add documents if they change significantly
6. **Bilingual**: Mix Hebrew and English documents freely
7. **Testing**: Always verify generated tests align with requirements
