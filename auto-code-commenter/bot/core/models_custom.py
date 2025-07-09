# app/core/models_custom.py
import requests
import json

class CustomModel:
    """A customizable model class for making API requests to external model endpoints.
    
    Attributes:
        endpoint (str): The API endpoint URL
        method (str): HTTP method (default: POST)
        headers (dict): Additional request headers
        body_template (dict): Template for constructing request body
        response_path (str): Dot-path to extract response data
        timeout (int): Request timeout in seconds (default: 10)
        retries (int): Number of retry attempts (default: 3)
        request_format (str): Request format - 'json' or 'form' (default: 'json')
    """
    def __init__(self, config):
        """Initialize CustomModel with configuration.
        
        Args:
            config (dict): Configuration dictionary containing:
                - endpoint: API endpoint URL
                - method: HTTP method (optional)
                - headers: Request headers (optional)
                - body_template: Request body template (optional)
                - response_path: Path to extract response (optional)
                - timeout: Request timeout (optional)
                - retries: Retry attempts (optional)
                - request_format: Request format (optional)
        """
        self.endpoint = config["endpoint"]
        self.method = config.get("method", "POST").upper()
        self.headers = config.get("headers", {})
        self.body_template = config.get("body_template", {})
        self.response_path = config.get("response_path")
        self.timeout = config.get("timeout", 10)
        self.retries = config.get("retries", 3)
        self.request_format = config.get("request_format", "json")

    def generate(self, prompt: str, temperature=0, max_tokens=512, stop=None):
        """Generate a response from the custom model.
        
        Args:
            prompt (str): Input prompt for the model
            temperature (float): Sampling temperature (default: 0)
            max_tokens (int): Maximum tokens to generate (default: 512)
            stop (str|None): Stop sequence (optional)
            
        Returns:
            The generated response from the model
            
        Raises:
            RuntimeError: If all retry attempts fail
        """
        # Build request body mapping using template keys or defaults
        body = {}
        body[self.body_template.get("prompt_key", "prompt")] = prompt
        body[self.body_template.get("temperature_key", "temperature")] = temperature
        body[self.body_template.get("max_tokens_key", "max_tokens")] = max_tokens
        if self.body_template.get("stop_key") and stop:
            body[self.body_template["stop_key"]] = stop

        # Format request based on specified format
        if self.request_format == "json":
            req_data = json.dumps(body)
            headers = {"Content-Type": "application/json", **self.headers}
        elif self.request_format == "form":
            req_data = body
            headers = {"Content-Type": "application/x-www-form-urlencoded", **self.headers}
        else:
            req_data = body
            headers = self.headers

        # Attempt request with retries
        for _ in range(self.retries or 1):
            try:
                resp = requests.request(
                    self.method,
                    self.endpoint,
                    headers=headers,
                    data=req_data if self.request_format != "json" else None,
                    json=body if self.request_format == "json" else None,
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                data = resp.json()
                # Extract nested response data using dot path
                if self.response_path:
                    for key in self.response_path.split('.'):
                        data = data[key]
                return data
            except Exception as e:
                print(f"Error calling custom model: {e}")
        raise RuntimeError("Failed to get response from custom model")