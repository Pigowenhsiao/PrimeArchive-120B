import json
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional

import requests

from src.lib.network_guard import enforce_local_only


def _parse_json_content(content: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        if "{" in content and "}" in content:
            start = content.find("{")
            end = content.rfind("}")
            snippet = content[start : end + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                return None
    return None


@dataclass
class LLMClient:
    base_url: str
    model_name: str
    temperature: float = 0.1
    top_p: float = 0.9
    repeat_penalty: float = 1.1
    max_tokens: int = 2048
    num_ctx: int = 8192
    timeout_seconds: int = 60
    max_retries: int = 3

    def generate(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        enforce_local_only(self.base_url)
        attempt = 0
        while True:
            try:
                response = requests.post(
                    self._endpoint(),
                    json=self._payload(system_prompt, user_prompt),
                    timeout=self.timeout_seconds,
                )
                response.raise_for_status()
                data = response.json()
                content = self._extract_content(data)
                parsed = _parse_json_content(content)
                if parsed is not None:
                    return parsed
                return {"raw": content}
            except requests.Timeout as exc:
                attempt += 1
                if attempt >= self.max_retries:
                    raise TimeoutError("LLM request timed out") from exc
                time.sleep(1)
            except requests.RequestException as exc:
                raise RuntimeError("LLM request failed") from exc

    def _endpoint(self) -> str:
        if self.base_url.endswith("/v1"):
            return f"{self.base_url}/chat/completions"
        if self.base_url.endswith("/api/generate"):
            return self.base_url
        return f"{self.base_url}/api/generate"

    def _payload(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        if self.base_url.endswith("/v1"):
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})
            return {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_tokens": self.max_tokens,
            }
        return {
            "model": self.model_name,
            "prompt": f"{system_prompt}\n\n{user_prompt}".strip(),
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "repeat_penalty": self.repeat_penalty,
                "num_ctx": self.num_ctx,
                "num_predict": self.max_tokens,
            },
        }

    @staticmethod
    def _extract_content(data: Dict[str, Any]) -> str:
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        return data.get("response", "")
