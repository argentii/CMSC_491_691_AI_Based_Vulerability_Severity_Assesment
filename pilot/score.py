"""CVSS v3.1 vector -> base score + severity band, using the official formula (cvss package)."""
from cvss import CVSS3


def band(score: float) -> str:
    if score == 0.0:
        return "None"
    if score < 4.0:
        return "Low"
    if score < 7.0:
        return "Medium"
    if score < 9.0:
        return "High"
    return "Critical"


def score(vector: str) -> tuple[float, str]:
    base = float(CVSS3(vector).scores()[0])
    return base, band(base)
