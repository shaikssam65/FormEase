import json, re
from typing import Any, Dict, Optional
from dateutil.parser import parse as date_parse
from models import FormData

def blank_form_dict() -> Dict[str, Any]:
    return FormData().model_dump()

def normalize_date(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    try:
        d = date_parse(value, dayfirst=False, yearfirst=False)
        return d.date().isoformat()
    except Exception:
        return value

def coerce_dates_in_form(form: Dict[str, Any]) -> Dict[str, Any]:
    date_paths = [
        "basic_personal_info.date_of_birth",
        "address_and_permits.permit_expiry_date",
        "employment.start_date",
        "housing.lease_start_date",
        "housing.lease_end_date",
    ]
    def set_path(d: Dict[str, Any], path: str, value: Any):
        parts = path.split("."); cur = d
        for p in parts[:-1]:
            cur = cur.get(p, {})
        cur[parts[-1]] = value
    def get_path(d: Dict[str, Any], path: str):
        cur = d
        for p in path.split("."):
            if isinstance(cur, list): return None
            cur = cur.get(p)
            if cur is None: return None
        return cur
    for p in date_paths:
        v = get_path(form, p)
        if isinstance(v, str): set_path(form, p, normalize_date(v))
    # dependents and education dates
    for dep in form.get("dependents_information", {}).get("dependents", []):
        if isinstance(dep, dict) and isinstance(dep.get("date_of_birth"), str):
            dep["date_of_birth"] = normalize_date(dep["date_of_birth"])
    for it in form.get("education", {}).get("items", []):
        if isinstance(it, dict):
            if isinstance(it.get("start_date"), str): it["start_date"] = normalize_date(it["start_date"])
            if isinstance(it.get("end_date"), str): it["end_date"] = normalize_date(it["end_date"])
    return form

def parse_json_strict(text: str) -> Optional[Dict[str, Any]]:
    m = re.search(r"\{[\s\S]*\}", text)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def deep_merge(base, patch):
    # Be defensive about inputs
    if not isinstance(base, dict):
        base = {}
    if not isinstance(patch, dict):
        return base

    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = deep_merge(base.get(k), v)
        else:
            if v is not None:
                base[k] = v
    return base
