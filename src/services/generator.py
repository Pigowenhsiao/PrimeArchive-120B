from __future__ import annotations

from typing import List, Dict, Any, Optional

from src.services.llm_client import LLMClient
from src.services.prompting import build_prompt


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
) -> List[Dict[str, Any]]:
    units = []
    for idx, chunk in enumerate(chunks, start=1):
        reference = references[idx - 1]
        if llm_client:
            system_prompt, user_prompt = build_prompt(chunk)
            response = llm_client.generate(system_prompt, user_prompt)
            unit = response.get("unit") or response
            if "reference" not in unit:
                unit["reference"] = reference
        else:
            unit = _fallback_unit(chunk, reference)
        units.append(unit)
    return units
