import time
from dataclasses import dataclass
from typing import Dict, Any

import requests

from src.lib.network_guard import enforce_local_only


@dataclass
class LLMClient:
    base_url: str
    timeout_seconds: int = 60
    max_retries: int = 3

    def generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        enforce_local_only(self.base_url)
        attempt = 0
        while True:
            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout_seconds,
                )
                response.raise_for_status()
                return response.json()
            except requests.Timeout as exc:
                attempt += 1
                if attempt >= self.max_retries:
                    raise TimeoutError("LLM request timed out") from exc
                time.sleep(1)
            except requests.RequestException as exc:
                raise RuntimeError("LLM request failed") from exc
