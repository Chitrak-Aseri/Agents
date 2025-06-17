from langchain_community.chat_models import ChatOpenAI
from langchain_deepseek import ChatDeepSeek


class ModelFactory:
    def __init__(self, config):
        self.single_model_config = config.get("model")
        self.multi_model_config = config.get("models")

    def get_llms(self):
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
            raise ValueError("No valid model configuration found. Please define `model:` or `models:` in your YAML.")

        return instances

    def _create_model(self, model_type, params):
        if model_type == "openai":
            return ChatOpenAI(**params)
        elif model_type == "deepseek":
            return ChatDeepSeek(**params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
