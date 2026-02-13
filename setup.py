"""Setup script for Knowledge Base system."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="knowledgebase",
    version="0.1.0",
    author="Knowledge Base Team",
    description="A knowledge base system for processing and analyzing process documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ofercell/knowledgebase",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-community>=0.0.20",
        "openai>=1.12.0",
        "pypdf>=3.17.0",
        "python-docx>=1.1.0",
        "Pillow>=10.0.0",
        "pytesseract>=0.3.10",
        "chromadb>=0.4.22",
        "python-dotenv>=1.0.0",
        "tiktoken>=0.5.2",
        "python-bidi>=0.4.2",
        "arabic-reshaper>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kb=kb_cli:main",
        ],
    },
)
