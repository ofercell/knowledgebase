#!/usr/bin/env python3
"""Command-line interface for the Knowledge Base system."""

import argparse
import sys
from pathlib import Path

from knowledgebase.knowledge_base import KnowledgeBase


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Knowledge Base System - Process documents and answer questions"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add document command
    add_parser = subparsers.add_parser("add", help="Add a document to the knowledge base")
    add_parser.add_argument("file", help="Path to the document file")
    
    # Ask question command
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Your question")
    ask_parser.add_argument(
        "--results",
        type=int,
        default=5,
        help="Number of context documents to use (default: 5)"
    )
    
    # Get insights command
    insights_parser = subparsers.add_parser("insights", help="Extract insights from documents")
    insights_parser.add_argument(
        "--document",
        help="Specific document name (optional)"
    )
    insights_parser.add_argument(
        "--max",
        type=int,
        default=10,
        help="Maximum number of insights (default: 10)"
    )
    
    # Generate tests command
    tests_parser = subparsers.add_parser("generate-tests", help="Generate test cases")
    tests_parser.add_argument(
        "--document",
        help="Specific document name (optional)"
    )
    tests_parser.add_argument(
        "--type",
        choices=["functional", "integration", "unit"],
        default="functional",
        help="Type of tests to generate (default: functional)"
    )
    
    # List documents command
    list_parser = subparsers.add_parser("list", help="List all documents in knowledge base")
    
    # Delete document command
    delete_parser = subparsers.add_parser("delete", help="Delete a document")
    delete_parser.add_argument("filename", help="Name of the document to delete")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show knowledge base statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        kb = KnowledgeBase()
        
        if args.command == "add":
            result = kb.add_document(args.file)
            print(f"\n✓ Document added successfully!")
            print(f"  Filename: {result['filename']}")
            print(f"  Chunks: {result['chunks_added']}")
            
        elif args.command == "ask":
            print(f"\nQuestion: {args.question}\n")
            result = kb.ask_question(args.question, args.results)
            
            print("Answer:")
            print(result['answer'])
            print("\nSources:")
            for idx, source in enumerate(result['sources'], 1):
                page_info = f" (Page {source['page_number']})" if source.get('page_number') else ""
                print(f"  {idx}. {source['filename']}{page_info}")
            
        elif args.command == "insights":
            print("\nExtracting insights...\n")
            insights = kb.get_insights(args.document, args.max)
            
            if insights:
                print("Key Insights:")
                for idx, insight in enumerate(insights, 1):
                    print(f"  {idx}. {insight}")
            else:
                print("No insights found.")
            
        elif args.command == "generate-tests":
            print(f"\nGenerating {args.type} test cases...\n")
            tests = kb.generate_tests(args.document, args.type)
            
            if tests:
                print(f"Generated {len(tests)} test cases:\n")
                for idx, test in enumerate(tests, 1):
                    print(f"--- Test Case {idx} ---")
                    print(test.get('full_text', ''))
                    print()
            else:
                print("No test cases generated.")
            
        elif args.command == "list":
            documents = kb.list_documents()
            
            if documents:
                print("\nDocuments in knowledge base:")
                for idx, doc in enumerate(documents, 1):
                    print(f"  {idx}. {doc}")
            else:
                print("\nNo documents in knowledge base.")
            
        elif args.command == "delete":
            result = kb.delete_document(args.filename)
            print(f"\n✓ Document deleted!")
            print(f"  Filename: {result['filename']}")
            print(f"  Chunks deleted: {result['chunks_deleted']}")
            
        elif args.command == "stats":
            stats = kb.get_stats()
            print("\nKnowledge Base Statistics:")
            print(f"  Total chunks: {stats['total_chunks']}")
            print(f"  Total documents: {stats['total_documents']}")
            if stats['documents']:
                print("\n  Documents:")
                for doc in stats['documents']:
                    print(f"    - {doc}")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
