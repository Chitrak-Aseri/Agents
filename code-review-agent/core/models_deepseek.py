# code-review-agent/core/models_deepseek.py
import os
from langchain_openai import ChatOpenAI

class DeepSeekModel:
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

        
        self.llm = ChatOpenAI(**init_params)

    def generate(self, prompt: str) -> str:
        return self.llm.predict(prompt)