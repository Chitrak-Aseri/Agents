# code-review-agent/core/models_deepseek.py
import os
from langchain_openai import ChatOpenAI

class DeepSeekModel:
    """A wrapper class for interacting with DeepSeek's OpenAI-compatible API.

    This class provides an interface to generate text completions using DeepSeek's models
    through the OpenAI API format.
    """
    def __init__(self, model_name, temperature=0, max_tokens=None, credentials=None, additional_params=None):
        """Initialize the DeepSeek model wrapper.

        Args:
            model_name: Name of the DeepSeek model to use
            temperature: Controls randomness (0 = deterministic, higher = more random)
            max_tokens: Maximum number of tokens to generate (not currently used)
            credentials: Dictionary containing API credentials (api_key, api_base)
            additional_params: Additional parameters for model configuration (not currently used)
        
        Raises:
            ValueError: If API key is not provided in credentials or environment
        """
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

        
        self.llm = ChatOpenAI(**init_params)

    def generate(self, prompt: str) -> str:
        """Generate text completion for the given prompt.

        Args:
            prompt: Input text to generate completion for

        Returns:
            str: Generated text completion from the model
        """
        print("--------------Start-Prompt------------------")
        print(prompt)
        print("--------------End-Prompt------------------")
        return self.llm.predict(prompt)