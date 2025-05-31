# code-review-agent/core/models_custom.py
import requests
import json

class CustomModel:
    def __init__(self, config):
        self.endpoint = config["endpoint"]
        self.method = config.get("method", "POST").upper()
        self.headers = config.get("headers", {})
        self.body_template = config.get("body_template", {})
        self.response_path = config.get("response_path")
        self.timeout = config.get("timeout", 10)
        self.retries = config.get("retries", 3)
        self.request_format = config.get("request_format", "json")

    def generate(self, prompt: str, temperature=0, max_tokens=512, stop=None):
        # Build request body mapping
        body = {}
        body[self.body_template.get("prompt_key", "prompt")] = prompt
        body[self.body_template.get("temperature_key", "temperature")] = temperature
        body[self.body_template.get("max_tokens_key", "max_tokens")] = max_tokens
        if self.body_template.get("stop_key") and stop:
            body[self.body_template["stop_key"]] = stop

        # Format request
        if self.request_format == "json":
            req_data = json.dumps(body)
            headers = {"Content-Type": "application/json", **self.headers}
        elif self.request_format == "form":
            req_data = body
            headers = {"Content-Type": "application/x-www-form-urlencoded", **self.headers}
        else:
            req_data = body
            headers = self.headers

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
                # Extract response text by dot path
                for key in self.response_path.split('.'):
                    data = data[key]
                return data
            except Exception as e:
                print(f"Error calling custom model: {e}")
        raise RuntimeError("Failed to get response from custom model")