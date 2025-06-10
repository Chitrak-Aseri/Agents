# code-review-agent/core/models_openai.py
import os
from langchain_openai import ChatOpenAI

class OpenAIModel:
    """Wrapper class for OpenAI chat models using LangChain's ChatOpenAI.
    
    Args:
        model_name (str): Name of the OpenAI model to use (e.g., 'gpt-3.5-turbo')
        temperature (float, optional): Sampling temperature for model generation. Defaults to 0.
        credentials (dict, optional): Dictionary containing API credentials. Defaults to None.
        additional_params (dict, optional): Additional parameters to pass to ChatOpenAI. Defaults to None.
    """
    def __init__(self, model_name, temperature=0, credentials=None, additional_params=None):
        """Initialize the OpenAI model with given parameters."""
        api_key = credentials.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            **(additional_params or {}),
        )

    def generate(self, prompt: str) -> str:
        """Generate text response from the model for the given prompt.
        
        Args:
            prompt (str): Input text prompt for the model
            
        Returns:
            str: Generated text response from the model
        """
        return self.llm.predict(prompt)