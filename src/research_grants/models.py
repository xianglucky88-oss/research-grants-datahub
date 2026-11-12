from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeAlias


@dataclass(frozen=True)
class GrantRecord:
    source: str
    record_key: str
    observed_at: str
    project_id: str
    title: str
    institution: str
    principal_investigator: str
    status: str
    award_amount: float
    start_date: str
    end_date: str
    payload: dict[str, Any]
    raw_hash: str


DOMAIN_RECORD_TYPE: TypeAlias = GrantRecord
