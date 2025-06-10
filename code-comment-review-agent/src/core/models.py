# code-review-agent/core/models.py
import os
from .models_openai import OpenAIModel
from .models_deepseek import DeepSeekModel
from .models_bedrock import get_bedrock_model
from .models_huggingface import HuggingFaceChatModel

# Add imports for other provider model wrappers here (e.g., GoogleGeminiModel, GroqModel, etc.)

def get_model_instance(config: dict):
    """Factory function to create and return an appropriate model instance based on configuration.
    
    Args:
        config (dict): Configuration dictionary containing:
            - provider: Dictionary with 'type' key specifying the model provider
            - model_name: Name of the model to use
            - temperature: Temperature parameter for model generation
            - credentials: Authentication credentials for the provider
            - additional_params: Extra parameters specific to the provider
            
    Returns:
        An instance of the requested model class
        
    Raises:
        ValueError: If the provider type is not supported
        NotImplementedError: For provider types that are not yet implemented
    """
    provider_cfg = config.get("provider", {})
    provider_type = provider_cfg.get("type")
    # print("------------------------------CREDS_MODELS---------------------")
    # print(config.get("credentials", {}))
    # print("------------------------------CREDS_MODELS---------------------")
    if provider_type == "openai":
        return OpenAIModel(
            model_name=config.get("model_name"),
            temperature=config.get("temperature", 0),
            credentials=config.get("credentials", {}),
            additional_params=config.get("additional_params", {}),
        )
    elif provider_type == "deepseek":
        return DeepSeekModel(
            model_name=config.get("model_name"),
            temperature=config.get("temperature", 0),
            credentials=config.get("credentials", {}),
        )
    elif provider_type == "bedrock":
        return get_bedrock_model(config)
    elif provider_type == "huggingface":
        return HuggingFaceChatModel(
            model_name=config.get("model_name", "microsoft/phi-4"),  # Default to phi-4 if not specified
            temperature=config.get("temperature", 0),
            credentials=config.get("credentials", {}),
        )
    elif provider_type == "google_gemini":
        raise NotImplementedError("Google Gemini model integration not yet implemented.")
    elif provider_type == "groq":
        raise NotImplementedError("Groq model integration not yet implemented.")
    elif provider_type == "custom":
        raise NotImplementedError("Custom model integration not yet implemented.")
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")