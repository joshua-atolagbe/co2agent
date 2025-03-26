"""
Configuration settings for the CO2 Storage Assessment system.
"""

# LLM and vector store configuration
SYSTEM_CONFIG = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "praison",
            "path": ".praison"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "ft:gpt-4o-mini-2024-07-18:personal:wellgptx200kttx10ep:Ac9OWaNh",
            "temperature": 0.1,
            # "presence_penalty": 0.1,         
            # "frequency_penalty": 0.1,        
            # "api_key": "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",                 
            # "base_url": None,                
            # "response_format": {             
            #     "type": "text"               
            # },
            # "seed": 42,                
        },
    },
    # Add cache configuration to improve retrieval performance
    "cache": {
        "enabled": True,
        "ttl": 3600,  # Cache time-to-live in seconds
        "directory": ".cache"
    }
}

# Global constants
LLM_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:wellgptx200kttx10ep:Ac9OWaNh"
KNOWLEDGE_FILES = ["reports/15_9_14_Well_completion_report.pdf"]
