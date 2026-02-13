"""Configuration management for the knowledge base system."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings for the knowledge base system."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Model Configuration
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Storage Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(DATA_DIR / "chromadb"))
    DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", str(DATA_DIR / "documents"))
    
    # Processing Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        Path(cls.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.DOCUMENTS_PATH).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in your .env file "
                "or environment variables."
            )


config = Config()
