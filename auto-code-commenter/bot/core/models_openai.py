# bot/core/models_openai.py
import os
from langchain_openai import ChatOpenAI

class OpenAIModel:
    """Wrapper class for OpenAI's chat models using LangChain's ChatOpenAI interface.
    
    Args:
        model_name (str): Name of the OpenAI model to use (e.g., 'gpt-3.5-turbo')
        temperature (float, optional): Controls randomness in output. Defaults to 0.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 1024.
        credentials (dict, optional): Dictionary containing API credentials. Defaults to None.
        additional_params (dict, optional): Additional parameters to pass to ChatOpenAI. Defaults to None.
    """
    def __init__(self, model_name, temperature=0, max_tokens=1024, credentials=None, additional_params=None):
        # Get API key from credentials or environment variable
        api_key = credentials.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            max_tokens=max_tokens,
            **(additional_params or {}),
        )

    def generate(self, prompt: str) -> str:
        """Generate a response from the model given an input prompt.
        
        Args:
            prompt (str): The input text prompt for the model
            
        Returns:
            str: The generated response from the model
        """
        return self.llm.predict(prompt)