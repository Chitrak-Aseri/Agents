from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI


class ModelFactory:
    """Factory class for creating and managing LLM (Large Language Model) instances.
    
    Args:
        config (dict): Configuration dictionary containing either 'model' (single model)
                       or 'models' (multiple models) configuration.
    """
    def __init__(self, config):
        self.single_model_config = config.get("model")
        self.multi_model_config = config.get("models")

    def get_llms(self):
        """Create and return LLM instances based on configuration.
        
        Returns:
            list: List of initialized LLM instances.
            
        Raises:
            ValueError: If no valid model configuration is found.
        """
        instances = []

        # If multi-model config exists
        if self.multi_model_config:
            for model_cfg in self.multi_model_config:
                model_type = model_cfg.get("type")
                params = model_cfg.get("params", {})
                instances.append(self._create_model(model_type, params))

        # Else fallback to single model config
        elif self.single_model_config:
            model_type = self.single_model_config.get("type")
            params = self.single_model_config.get("params", {})
            instances.append(self._create_model(model_type, params))

        else:
            raise ValueError(
                "No valid model configuration found. Please define `model:` or `models:` in your YAML."
            )

        return instances

    def _create_model(self, model_type, params):
        """Internal method to create a specific model instance.
        
        Args:
            model_type (str): Type of model to create ('openai' or 'deepseek').
            params (dict): Parameters to pass to the model constructor.
            
        Returns:
            object: Initialized model instance.
            
        Raises:
            ValueError: If an unsupported model type is provided.
        """
        if model_type == "openai":
            return ChatOpenAI(**params)
        elif model_type == "deepseek":
            return ChatDeepSeek(**params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")