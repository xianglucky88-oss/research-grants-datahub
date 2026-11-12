from __future__ import annotations

from .models import GrantRecord


def validate(record: GrantRecord) -> list[str]:
    issues: list[str] = []

    if record.award_amount > 10_000_000_000:
        issues.append("award_amount is unusually large")

    return issues
