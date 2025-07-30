from typing import Optional

ACADEMIC_KEYWORDS = [
    "university", "college", "school", "institute", "department",
    "faculty", "hospital", "clinic", "center", "centre", "research",
    "laboratory", "med school"
]

def is_academic_affiliation(affiliation: str) -> bool:
    """
    Return True if the affiliation appears to be academic.
    """
    affil_lower = affiliation.lower()
    return any(keyword in affil_lower for keyword in ACADEMIC_KEYWORDS)

def extract_email(affiliation: str) -> Optional[str]:
    """
    Extract email address from affiliation text, if present.
    """
    import re
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
    return match.group(0) if match else None
