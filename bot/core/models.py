# app/core/models.py
import os
from bot.core.models_openai import OpenAIModel
from bot.core.models_deepseek import DeepSeekModel
from bot.core.models_bedrock import get_bedrock_model

# Add imports for other provider model wrappers here

def get_model_instance(config: dict):
    provider_cfg = config.get("provider", {})
    provider_type = provider_cfg.get("type")

    if provider_type == "openai":
        return OpenAIModel(
            model_name=config.get("model_name"),
            temperature=config.get("temperature", 0),
            credentials=config.get("credentials", {}),
            additional_params=config.get("additional_params", {}),
        )
    # elif provider_type == "deepseek":
    #     return DeepSeekModel(
    #         model_name=config.get("model_name"),
    #         temperature=config.get("temperature", 0),
    #         credentials=config.get("credentials", {}),
    #     )
    elif provider_type == "bedrock":
        return get_bedrock_model(config)
    elif provider_type == "huggingface":
        # Return HuggingFaceModel(...)
        pass
    elif provider_type == "google_gemini":
        # Return GoogleGeminiModel(...)
        pass
    elif provider_type == "groq":
        # Return GroqModel(...)
        pass
    elif provider_type == "custom":
        # Return CustomModel(...)
        pass
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")
