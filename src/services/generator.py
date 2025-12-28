from __future__ import annotations

import json
from typing import List, Dict, Any, Optional

from src.services.llm_client import LLMClient
from src.services.prompting import build_prompt


REQUIRED_FIELDS = {"concept", "description", "application", "tags", "type"}
OPTIONAL_FIELDS = {"confidence", "reference"}


def _normalize_tags(tags: Any) -> List[str]:
    if isinstance(tags, list):
        flattened: List[str] = []
        for item in tags:
            if isinstance(item, list):
                flattened.extend(str(sub).strip() for sub in item)
            else:
                flattened.append(str(item).strip())
        return [tag for tag in flattened if tag]
    if tags is None:
        return []
    return [str(tags).strip()]


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _sanitize_unit(unit: Dict[str, Any], reference: str) -> Dict[str, Any]:
    cleaned = {k: v for k, v in unit.items() if k in REQUIRED_FIELDS | OPTIONAL_FIELDS}
    if "tags" in cleaned:
        cleaned["tags"] = _normalize_tags(cleaned["tags"])
    if "application" in cleaned:
        cleaned["application"] = _stringify(cleaned["application"])
    if "reference" in cleaned:
        cleaned["reference"] = _stringify(cleaned["reference"])
    if "reference" not in cleaned:
        cleaned["reference"] = reference
    if not REQUIRED_FIELDS.issubset(cleaned.keys()):
        raise ValueError("Missing required fields")
    return cleaned


def _fallback_unit(chunk: str, reference: str) -> Dict[str, Any]:
    words = chunk.split()
    concept = " ".join(words[:5]) if words else "Untitled"
    return {
        "concept": concept,
        "description": chunk[:200],
        "application": "knowledge_extraction",
        "tags": ["auto"],
        "type": "concept",
        "reference": reference,
    }


def generate_units(
    chunks: List[str],
    references: List[str],
    llm_client: Optional[LLMClient] = None,
    print_llm_output: bool = False,
) -> List[Dict[str, Any]]:
    units = []
    for idx, chunk in enumerate(chunks, start=1):
        reference = references[idx - 1]
        if llm_client:
            system_prompt, user_prompt = build_prompt(chunk)
            response = llm_client.generate(system_prompt, user_prompt)
            if print_llm_output:
                print(f"LLM output (chunk {idx}): {response}")
            candidate = response.get("unit") or response
            if isinstance(candidate, list) and candidate:
                candidate = candidate[0]
            try:
                unit = _sanitize_unit(candidate, reference)
            except ValueError:
                unit = _fallback_unit(chunk, reference)
        else:
            unit = _fallback_unit(chunk, reference)
        units.append(unit)
    return units
