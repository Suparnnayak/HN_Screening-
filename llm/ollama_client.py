# llm/ollama_client.py

import requests
import json
from typing import Optional
from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL_NAME,
    MAX_LLM_RETRIES,
    LLM_TIMEOUT_SECONDS
)


class OllamaClient:
    """
    Production-safe client for Ollama (local LLM).
    """

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model_name: str = OLLAMA_MODEL_NAME
    ):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.endpoint = f"{self.base_url}/api/generate"

    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to Ollama and returns raw JSON response string.
        Retries on failure.
        """

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        last_error: Optional[Exception] = None

        for attempt in range(1, MAX_LLM_RETRIES + 1):
            try:
                response = requests.post(
                    self.endpoint,
                    json=payload,
                    timeout=LLM_TIMEOUT_SECONDS
                )

                response.raise_for_status()

                data = response.json()

                if "response" not in data:
                    raise ValueError("Ollama response missing 'response' field")

                text = data["response"].strip()
                if not text:
                    print(f"DEBUG: Empty response from Ollama. Full data: {data}")
                    raise ValueError("Empty response from LLM")

                print(f"DEBUG: Ollama raw response: {text[:500]}")

                # Strict JSON validation
                json.loads(text)

                return text

            except Exception as e:
                last_error = e
                if attempt == MAX_LLM_RETRIES:
                    break

        raise RuntimeError(
            f"LLM generation failed after {MAX_LLM_RETRIES} attempts"
        ) from last_error
