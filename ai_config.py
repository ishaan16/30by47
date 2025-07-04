"""
Configuration for AI-powered insights.
Set your preferred LLM provider and API keys here.
"""

# LLM Provider Configuration
LLM_PROVIDER = "enhanced_static"  # Options: "enhanced_static", "openai", "huggingface", "local_llm"

# API Keys (set these as environment variables)
# OPENAI_API_KEY = "your_openai_api_key_here"
# HUGGINGFACE_API_KEY = "your_huggingface_api_key_here"

# Local LLM Configuration (for Ollama)
LOCAL_LLM_URL = "http://localhost:11434/api/generate"
LOCAL_LLM_MODEL = "llama2"  # or "mistral", "codellama", etc.

# Enhanced Static Insights Configuration
ENABLE_SECTOR_RANKINGS = True
ENABLE_YEAR_CONTEXT = True
ENABLE_PERCENTAGE_CONTEXT = True

# Insight Customization
INSIGHT_STYLE = "professional"  # Options: "professional", "casual", "technical"
MAX_INSIGHT_LENGTH = 200  # Maximum characters for insights 