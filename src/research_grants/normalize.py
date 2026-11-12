from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import GrantRecord
from .identity import record_key


def _text(value: Any) -> str:
    return " ".join(str(value).split()) if value is not None else ""


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("numeric field is invalid") from exc


def normalize(raw: Any, source: str) -> GrantRecord:
    if not isinstance(raw, dict):
        raise ValueError("record must be an object")
    payload = raw.get("payload")
    observed_at = _text(raw.get("observed_at"))
    if not isinstance(payload, dict) or not observed_at:
        raise ValueError("observed_at and object payload are required")

    project_id = _text(payload.get("project_id"))
    title = _text(payload.get("title"))
    institution = _text(payload.get("institution"))
    principal_investigator = _text(payload.get("principal_investigator"))
    status = _text(payload.get("status")).lower()
    award_amount = _number(payload.get("award_amount"))
    start_date = _text(payload.get("start_date"))
    end_date = _text(payload.get("end_date"))
    if not project_id or not title or not institution or not status or not start_date or not end_date:
        raise ValueError("project_id, title, institution, status and dates are required")
    if status not in {"announced", "under_review", "awarded", "active", "completed", "terminated"}:
        raise ValueError("unsupported grant status")
    if award_amount is None or award_amount < 0:
        raise ValueError("award_amount must be non-negative")
    if end_date < start_date:
        raise ValueError("end_date must not be earlier than start_date")

    normalized = {"project_id": project_id, "title": title, "institution": institution, "principal_investigator": principal_investigator, "status": status, "award_amount": award_amount, "start_date": start_date, "end_date": end_date}
    key = record_key(project_id, observed_at)
    canonical = json.dumps({"source": source, "observed_at": observed_at, "payload": normalized}, ensure_ascii=False, sort_keys=True)
    raw_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return GrantRecord(
        source=source,
        record_key=key,
        observed_at=observed_at,
        project_id=normalized["project_id"],
        title=normalized["title"],
        institution=normalized["institution"],
        principal_investigator=normalized["principal_investigator"],
        status=normalized["status"],
        award_amount=normalized["award_amount"],
        start_date=normalized["start_date"],
        end_date=normalized["end_date"],
        payload=normalized,
        raw_hash=raw_hash,
    )
