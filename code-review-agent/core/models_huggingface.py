# code-review-agent/core/models_huggingface.py

import os
import requests

class HuggingFaceChatModel:
    def __init__(self, model_name="google/gemma-3-27b-it-fast", temperature=0.7, credentials=None):
        credentials = credentials or {}

        self.api_key = credentials.get("HF_TOKEN") or os.getenv("HF_TOKEN")
        if not self.api_key:
            raise ValueError("HuggingFace API key not provided in config or environment")

        self.model_name = model_name
        self.temperature = temperature
        self.api_base = self.api_base = credentials.get("api_base") or os.getenv("HF_API_BASE_URL")
        print("********************************************")
        print(self.api_base +" <----------------------------> "+ self.model_name)
        print("********************************************")
    def generate(self, prompt: str) -> str:
        print("--------------Start-Prompt------------------")
        print(prompt)
        print("--------------End-Prompt--------------------")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "temperature": self.temperature,
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        }

        response = requests.post(f"{self.api_base}/chat/completions", headers=headers, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"HF API error {response.status_code}: {response.text}")
        data = response.json()
        print(data["choices"][0]["message"]["content"])
        return data["choices"][0]["message"]["content"]
