import json
from typing import Any, Dict

from llm import llm_generate
from utils import blank_form_dict, parse_json_strict

def category_schema(root_key: str) -> Dict[str, Any]:
    """
    Returns only the schema for the requested root key, e.g. {'employment': {...}}.
    """
    full = blank_form_dict()
    if root_key not in full:
        return {}
    return {root_key: full[root_key]}

def _copy_known(dst: Dict[str, Any], src: Dict[str, Any]) -> None:
    """
    Copy only keys that already exist in dst (schema-safe).
    """
    for k in dst.keys():
        if isinstance(dst[k], dict):
            if isinstance(src.get(k), dict):
                _copy_known(dst[k], src[k])
        else:
            val = src.get(k)
            if val is not None:
                dst[k] = val

def extract_category(tokenizer, model, root_key: str, user_text: str) -> Dict[str, Any]:
    """
    Runs a scoped extraction for a single category.
    - tokenizer/model: loaded via llm.load_llm in app.py
    - root_key: one of the top-level keys in the form schema (e.g., 'employment')
    - user_text: free text pasted by user for that category
    Returns a dict patch like {'employment': {...}} suitable for deep_merge.
    """
    schema = category_schema(root_key)
    if not schema:
        # If the key is unknown, return an empty patch
        return {}

    system = {
        "role": "system",
        "content": (
            "You are a strict information extractor for migrant intake.\n"
            "Return ONLY a JSON object that matches the given category schema exactly.\n"
            "Rules:\n"
            "1) Keep the exact structure and keys under the ROOT key.\n"
            "2) Use null when unknown; do not fabricate values.\n"
            "3) Convert dates to YYYY-MM-DD when possible.\n"
            "4) No extra keys. No commentary."
        )
    }
    user = {
        "role": "user",
        "content": f"ROOT SCHEMA:\n{json.dumps(schema, indent=2)}\n\nUSER TEXT:\n{user_text}\n\nReturn JSON now."
    }

    # Generate and parse
    raw = llm_generate(tokenizer, model, [system, user], max_new_tokens=700, temperature=0.0)
    parsed = parse_json_strict(raw) or {}

    # Start from a clean schema for this root
    clean = category_schema(root_key)

    # Only copy recognized keys
    if root_key in parsed and isinstance(parsed[root_key], dict) and isinstance(clean.get(root_key), dict):
        _copy_known(clean[root_key], parsed[root_key])
    elif root_key in parsed and isinstance(parsed[root_key], list) and isinstance(clean.get(root_key), list):
        # for list-rooted sections (if any in the future)
        clean[root_key] = parsed[root_key]

    # Defensive return: always a dict patch
    return clean if isinstance(clean, dict) else {}
