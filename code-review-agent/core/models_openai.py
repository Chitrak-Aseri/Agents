# code-review-agent/core/models_openai.py
import os
from langchain_openai import ChatOpenAI

class OpenAIModel:
    def __init__(self, model_name, temperature=0, credentials=None, additional_params=None):
        api_key = credentials.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            **(additional_params or {}),
        )

    def generate(self, prompt: str) -> str:
        return self.llm.predict(prompt)