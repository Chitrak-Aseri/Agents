# code-review-agent/core/models_bedrock.py

from langchain_aws import BedrockLLM
import json

class WrappedBedrockModel:
    def __init__(self, model_id, region, credentials, model_kwargs=None):
        self.llm = BedrockLLM(
            model_id=model_id,
            region_name=region,
            model_kwargs=model_kwargs or {},
            credentials_profile_name=credentials.get("profile_name", None),
            aws_access_key_id=credentials.get("aws_access_key_id"),
            aws_secret_access_key=credentials.get("aws_secret_access_key"),
            aws_session_token=credentials.get("aws_session_token"),
        )

    def generate(self, prompt: str):
        print("PROMPT BEING SENT TO BEDROCK:\n", prompt)
        response= self.llm.invoke(prompt)
        print("-----------------------RESPONSE-START---------------------------")
        print(response)
        print("-----------------------RESPONSE-END-----------------------------")
        return response


def get_bedrock_model(model_cfg: dict):
    return WrappedBedrockModel(
        model_id=model_cfg.get("model_name", "meta.llama3-70b-instruct-v1:0"),
        region=model_cfg.get("region", "us-east-1"),
        credentials=model_cfg.get("credentials", {}),
        model_kwargs={
            "temperature": model_cfg.get("temperature", 1.0)
        },
    )