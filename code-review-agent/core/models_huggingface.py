# import os
# from langchain_community.llms import HuggingFaceHub
# from huggingface_hub import InferenceClient

# class HuggingFacePhiModel:
#     def __init__(self, model_name="microsoft/phi-4", temperature=0.7, credentials=None):
#         if credentials is None:
#             credentials = {}

#         self.api_key = credentials.get("HUGGINGFACE_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
#         if not self.api_key:
#             raise ValueError("HuggingFace API key not provided in config or environment")

#         # Initialize HuggingFace model using LangChain
#         self.llm = HuggingFaceHub(
#             repo_id=model_name,
#             huggingfacehub_api_token=self.api_key,
#             model_kwargs={"temperature": temperature}
#         )

#     def generate(self, prompt: str) -> str:
#         print("--------------Start-Prompt------------------")
#         print(prompt)
#         print("--------------End-Prompt------------------")
#         response = self.client.query(prompt)  

#         if not response:
#             raise RuntimeError("Failed to get response from Hugging Face model")

#         return str(response)


# def get_model_instance(config: dict) -> HuggingFacePhiModel:
#     provider_cfg = config.get("provider", {})
#     provider_type = provider_cfg.get("type")

#     if provider_type == "huggingface":
#         return HuggingFacePhiModel(
#             model_name=config.get("model_name", "microsoft/phi-4"),
#             temperature=config.get("temperature", 0.7),
#             credentials=config.get("credentials", {}),
#         )
#     else:
#         raise ValueError(f"Unsupported provider type: {provider_type}")
    

import os
import requests
from huggingface_hub import InferenceClient

class HuggingFacePhiModel:
    def __init__(self, model_name="microsoft/phi-4", temperature=0.7, credentials=None):
        if credentials is None:
            credentials = {}

        self.api_key = credentials.get("HUGGINGFACE_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        if not self.api_key:
            raise ValueError("HuggingFace API key not provided in config or environment")

        # Initialize Hugging Face Inference Client
        self.client = InferenceClient(model_name, token=self.api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate response using Hugging Face Microsoft Phi-4 model.

        Args:
            prompt (str): The text prompt for AI generation.

        Returns:
            str: AI-generated response.
        """
        print("--------------Start-Prompt------------------")
        print(prompt)
        print("--------------End-Prompt------------------")

        API_URL = f"https://api-inference.huggingface.co/models/{self.client.model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        data = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=data)  # ✅ Correct method

        if response.status_code != 200:
            raise RuntimeError(f"API call failed: {response.status_code} - {response.text}")

        return response.json()

def get_model_instance(config: dict) -> HuggingFacePhiModel:
    """
    Retrieve an instance of HuggingFacePhiModel based on configuration.

    Args:
        config (dict): Model configuration parameters.

    Returns:
        HuggingFacePhiModel: Instance of the Hugging Face AI model.
    """
    provider_cfg = config.get("provider", {})
    provider_type = provider_cfg.get("type")

    if provider_type == "huggingface":
        return HuggingFacePhiModel(
            model_name=config.get("model_name", "microsoft/phi-4"),
            temperature=config.get("temperature", 0.7),
            credentials=config.get("credentials", {}),
        )
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")

