import logging
from typing import Optional

import requests

from config.settings import (
    OPENAI_API_KEY,
    LLM_MODEL,
)


print("Shubham Sharma 23051870")


logger = logging.getLogger(__name__)


class LLMClient:
    """
    Client for communicating with the OpenAI Chat Completions API.

    Responsibilities:
    - Manage API configuration.
    - Send prompts to the configured model.
    - Validate API responses.
    - Log failures and propagate errors to the caller.

    The decision orchestration layer is responsible for
    selecting the appropriate fallback when an API call fails.
    """

    API_URL = "https://api.openai.com/v1/chat/completions"
    REQUEST_TIMEOUT = 60

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.api_key = (
            api_key
            if api_key is not None
            else OPENAI_API_KEY
        )

        self.model = (
            model
            if model is not None
            else LLM_MODEL
        )

        self.timeout = (
            timeout
            if timeout is not None
            else self.REQUEST_TIMEOUT
        )

        self.session = requests.Session()

    @property
    def available(self) -> bool:
        """
        Return whether the required API configuration exists.

        This checks configuration only. It does not guarantee
        that the API is reachable or that the credentials work.
        """
        return bool(
            self.api_key
            and self.api_key.strip()
            and self.model
            and self.model.strip()
        )

    def generate(self, prompt: str) -> str:
        """
        Generate a response using the configured LLM.

        Raises:
            ValueError:
                If the prompt is invalid or API configuration
                is missing.

            requests.RequestException:
                If the HTTP request fails.

            RuntimeError:
                If the API response is invalid or contains
                no usable assistant response.
        """

        if not isinstance(prompt, str):
            raise TypeError(
                "Prompt must be a string."
            )

        prompt = prompt.strip()

        if not prompt:
            raise ValueError(
                "Prompt cannot be empty."
            )

        if not self.available:
            raise ValueError(
                "LLM API is not configured. "
                "Check OPENAI_API_KEY and LLM_MODEL."
            )

        headers = {
            "Authorization": (
                f"Bearer {self.api_key}"
            ),
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.2,
        }

        try:
            response = self.session.post(
                self.API_URL,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.RequestException:
            logger.exception(
                "OpenAI API request failed."
            )
            raise

        try:
            data = response.json()

        except ValueError as error:
            logger.exception(
                "OpenAI API returned invalid JSON."
            )

            raise RuntimeError(
                "The LLM API returned an invalid response."
            ) from error

        try:
            content = data["choices"][0]["message"]["content"]

        except (
            KeyError,
            IndexError,
            TypeError,
        ) as error:
            logger.error(
                "OpenAI API response has an unexpected structure."
            )

            raise RuntimeError(
                "The LLM API response did not contain "
                "a valid assistant message."
            ) from error

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(
                "The LLM API returned an empty assistant response."
            )

        return content.strip()

