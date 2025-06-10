# code-review-agent/core/models_bedrock.py

from langchain_aws import BedrockLLM
import json

class WrappedBedrockModel:
    """Wrapper class for Bedrock LLM models with enhanced logging capabilities.
    
    Attributes:
        llm (BedrockLLM): The underlying Bedrock language model instance.
    """
    def __init__(self, model_id, region, credentials, model_kwargs=None):
        """Initialize the Bedrock model wrapper.
        
        Args:
            model_id (str): The Bedrock model identifier.
            region (str): AWS region for the Bedrock service.
            credentials (dict): AWS credentials dictionary containing:
                - profile_name (str, optional): AWS profile name
                - aws_access_key_id (str): AWS access key ID
                - aws_secret_access_key (str): AWS secret access key
                - aws_session_token (str, optional): AWS session token
            model_kwargs (dict, optional): Additional model parameters.
        """
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
        """Generate a response from the model with detailed logging.
        
        Args:
            prompt (str): The input prompt for the model.
            
        Returns:
            str: The model's generated response.
        """
        print("PROMPT BEING SENT TO BEDROCK:\n", prompt)
        response= self.llm.invoke(prompt)
        print("-----------------------RESPONSE-START---------------------------")
        print(response)
        print("-----------------------RESPONSE-END-----------------------------")
        return response


def get_bedrock_model(model_cfg: dict):
    """Factory function to create a configured WrappedBedrockModel instance.
    
    Args:
        model_cfg (dict): Configuration dictionary containing:
            - model_name (str, optional): Model ID (default: "meta.llama3-70b-instruct-v1:0")
            - region (str, optional): AWS region (default: "us-east-1")
            - credentials (dict, optional): AWS credentials
            - temperature (float, optional): Model temperature parameter (default: 1.0)
            
    Returns:
        WrappedBedrockModel: Configured model wrapper instance.
    """
    return WrappedBedrockModel(
        model_id=model_cfg.get("model_name", "meta.llama3-70b-instruct-v1:0"),
        region=model_cfg.get("region", "us-east-1"),
        credentials=model_cfg.get("credentials", {}),
        model_kwargs={
            "temperature": model_cfg.get("temperature", 1.0)
        },
    )