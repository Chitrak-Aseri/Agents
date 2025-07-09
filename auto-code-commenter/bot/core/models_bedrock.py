# app/core/models_bedrock.py

from langchain_aws import BedrockLLM
import json

class WrappedBedrockModel:
    """Wrapper class for Bedrock LLM with simplified interface and credential handling.
    
    Args:
        model_id: The Bedrock model identifier
        region: AWS region for the Bedrock service
        credentials: Dictionary containing AWS credentials (profile_name, access keys, etc.)
        model_kwargs: Additional model-specific parameters
    """
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
        """Generate a response from the Bedrock model for the given prompt.
        
        Args:
            prompt: Input text to send to the model
            
        Returns:
            The model's generated response
        """
        print("PROMPT BEING SENT TO BEDROCK:\n", prompt)
        return self.llm.invoke(prompt)


def get_bedrock_model(model_cfg: dict):
    """Factory function to create a configured WrappedBedrockModel instance.
    
    Args:
        model_cfg: Configuration dictionary containing:
            - model_name: Bedrock model ID (default: meta.llama3-70b-instruct-v1:0)
            - region: AWS region (default: us-east-1)
            - credentials: AWS credential dictionary
            - temperature: Model temperature parameter (default: 1.0)
            
    Returns:
        Configured WrappedBedrockModel instance
    """
    return WrappedBedrockModel(
        model_id=model_cfg.get("model_name", "meta.llama3-70b-instruct-v1:0"),
        region=model_cfg.get("region", "us-east-1"),
        credentials=model_cfg.get("credentials", {}),
        model_kwargs={
            "temperature": model_cfg.get("temperature", 1.0),
            "top_p" : 1.0  # Always use top_p=1.0 unless overridden
        },
    )