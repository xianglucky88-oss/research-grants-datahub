def record_key(project_id: str, observed_at: str) -> str:
    return "|".join(value.strip().upper() for value in (project_id, observed_at))

def institution_key(name: str) -> str:
    return " ".join(name.casefold().split())

def project_key(project_id: str) -> str:
    return project_id.strip().upper()
