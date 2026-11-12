STATUSES = ("announced", "under_review", "awarded", "active", "completed", "terminated")


def can_transition(previous: str, current: str) -> bool:
    if previous == current:
        return True
    allowed = {
        "announced": {"under_review", "awarded", "terminated"},
        "under_review": {"awarded", "terminated"},
        "awarded": {"active", "terminated"},
        "active": {"completed", "terminated"},
        "completed": set(),
        "terminated": set(),
    }
    return current in allowed.get(previous, set())
