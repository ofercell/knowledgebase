"""Question Answering system for the knowledge base."""

from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI

from ..config import config
from ..storage import KnowledgeStore


class QASystem:
    """Question answering system using the knowledge base."""
    
    def __init__(self, knowledge_store: KnowledgeStore):
        """
        Initialize the QA system.
        
        Args:
            knowledge_store: KnowledgeStore instance for retrieving context
        """
        self.knowledge_store = knowledge_store
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=config.OPENAI_API_KEY
        )
        
        # System prompt that handles Hebrew and English
        self.system_prompt = """You are a helpful assistant that answers questions based on the provided context from process documents.

The documents may contain:
- Functional specifications
- Technical specifications
- Working instructions
- Hebrew text and English text
- References to images and diagrams

Guidelines:
1. Answer based ONLY on the provided context
2. If the context doesn't contain the answer, say so clearly
3. Support both Hebrew and English questions
4. Provide detailed, accurate answers
5. Reference specific documents or sections when relevant
6. If asked about images or diagrams, mention that they exist in the documents

Context:
{context}

Question: {question}

Answer:"""
    
    def answer_question(
        self,
        question: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Answer a question using the knowledge base.
        
        Args:
            question: The question to answer
            n_results: Number of context documents to retrieve
            
        Returns:
            Dictionary containing answer and sources
        """
        # Retrieve relevant context
        search_results = self.knowledge_store.search(
            query=question,
            n_results=n_results
        )
        
        if not search_results:
            return {
                "answer": "I don't have any relevant information in the knowledge base to answer this question.",
                "sources": [],
                "context_used": []
            }
        
        # Build context from search results
        context_parts = []
        sources = []
        
        for idx, result in enumerate(search_results):
            content = result["content"]
            metadata = result["metadata"]
            
            context_parts.append(f"[Document {idx + 1}]: {content}")
            
            source_info = {
                "filename": metadata.get("filename", "Unknown"),
                "page_number": metadata.get("page_number"),
                "chunk_index": metadata.get("chunk_index")
            }
            sources.append(source_info)
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        prompt = self.system_prompt.format(
            context=context,
            question=question
        )
        
        # Get answer from LLM
        response = self.llm.invoke(prompt)
        answer = response.content
        
        return {
            "answer": answer,
            "sources": sources,
            "context_used": [
                r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"]
                for r in search_results
            ]
        }
    
    def extract_insights(
        self,
        document_name: Optional[str] = None,
        max_insights: int = 10
    ) -> List[str]:
        """
        Extract key insights from documents.
        
        Args:
            document_name: Optional specific document to analyze
            max_insights: Maximum number of insights to extract
            
        Returns:
            List of insight strings
        """
        # Get relevant chunks
        if document_name:
            search_results = self.knowledge_store.search(
                query="key points important information insights",
                n_results=max_insights,
                filter_metadata={"filename": document_name}
            )
        else:
            search_results = self.knowledge_store.search(
                query="key points important information insights",
                n_results=max_insights
            )
        
        if not search_results:
            return []
        
        # Build context
        context = "\n\n".join([
            f"Excerpt {idx + 1}: {result['content']}"
            for idx, result in enumerate(search_results)
        ])
        
        # Create prompt for insights extraction
        prompt = f"""Based on the following excerpts from process documents, extract the key insights, important points, and critical information.

Provide a numbered list of distinct insights.

Excerpts:
{context}

Key Insights:"""
        
        # Get insights from LLM
        response = self.llm.invoke(prompt)
        insights_text = response.content
        
        # Parse insights (assuming numbered list)
        insights = []
        for line in insights_text.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-") or line.startswith("•")):
                # Remove numbering and bullets
                insight = line.lstrip("0123456789.-•) ").strip()
                if insight:
                    insights.append(insight)
        
        return insights[:max_insights]
    
    def generate_tests(
        self,
        document_name: Optional[str] = None,
        test_type: str = "functional"
    ) -> List[Dict[str, str]]:
        """
        Generate test cases from documentation.
        
        Args:
            document_name: Optional specific document to generate tests from
            test_type: Type of tests to generate (functional, integration, unit)
            
        Returns:
            List of test case dictionaries
        """
        # Get relevant chunks
        if document_name:
            search_query = f"{test_type} requirements specifications test cases"
            search_results = self.knowledge_store.search(
                query=search_query,
                n_results=5,
                filter_metadata={"filename": document_name}
            )
        else:
            search_query = f"{test_type} requirements specifications test cases"
            search_results = self.knowledge_store.search(
                query=search_query,
                n_results=5
            )
        
        if not search_results:
            return []
        
        # Build context
        context = "\n\n".join([
            f"Section {idx + 1}: {result['content']}"
            for idx, result in enumerate(search_results)
        ])
        
        # Create prompt for test generation
        prompt = f"""Based on the following documentation, generate {test_type} test cases.

For each test case, provide:
1. Test ID
2. Test Description
3. Prerequisites
4. Test Steps
5. Expected Results

Format each test case clearly and number them.

Documentation:
{context}

Test Cases:"""
        
        # Get test cases from LLM
        response = self.llm.invoke(prompt)
        test_cases_text = response.content
        
        # Parse test cases (basic parsing)
        test_cases = []
        current_test = {}
        
        for line in test_cases_text.split("\n"):
            line = line.strip()
            
            if "Test ID" in line or "Test Case" in line:
                if current_test:
                    test_cases.append(current_test)
                current_test = {"full_text": line}
            elif current_test:
                current_test["full_text"] = current_test.get("full_text", "") + "\n" + line
        
        if current_test:
            test_cases.append(current_test)
        
        return test_cases
