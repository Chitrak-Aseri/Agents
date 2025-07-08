# bot/core/models_deepseek.py
import os
from langchain_openai import ChatOpenAI

class DeepSeekModel:
    """Wrapper for DeepSeek's OpenAI-compatible API interface.
    
    Args:
        model_name: Name of the DeepSeek model to use
        temperature: Controls randomness (0 = deterministic)
        max_tokens: Maximum number of tokens to generate (optional)
        credentials: Dict containing 'api_key' and optionally 'api_base'
        additional_params: Additional parameters for model initialization (unused in current implementation)
    """
    def __init__(self, model_name, temperature=0, max_tokens=None, credentials=None, additional_params=None):
        # DeepSeek uses OpenAI-compatible API interface
        self.api_key = credentials.get("api_key") or os.getenv("DEEPSEEK_API_KEY")
        self.api_base = credentials.get("api_base") or os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

        if not self.api_key:
            raise ValueError("DeepSeek API key not provided in config or environment")
        init_params = {
            'model_name': model_name,
            'temperature': temperature,
            'openai_api_key': self.api_key,
            'openai_api_base': self.api_base,
        }

        # Initialize LangChain's OpenAI client with DeepSeek's API parameters
        self.llm = ChatOpenAI(**init_params)

    def generate(self, prompt: str) -> str:
        """Generate text completion for the given prompt.
        
        Args:
            prompt: Input text to send to the model
            
        Returns:
            str: Generated text completion
        """
        return self.llm.predict(prompt)