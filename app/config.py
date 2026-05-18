import os
from dotenv import load_dotenv

# Load environment variables from the local .env file into os.environ
load_dotenv()


class Settings:
    """
    Core application settings.
    
    Acts as the single source of truth for configuration across the entire project.
    Values are securely pulled from environment variables with sensible defaults fallback.
    """
    PROJECT_NAME: str = "Query Intelligence API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Anthropic API key used to authenticate requests to Claude
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY")
    
    # File path for the local SQLite database
    DB_PATH: str = os.environ.get("DB_PATH", "queries.db")


# Instantiate settings once to be imported and shared across the application
settings = Settings()
