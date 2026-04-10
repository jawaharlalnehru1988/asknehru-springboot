import json
from pathlib import Path


MAIN_TOPICS = [
    {"value": "JAVA", "label": "Java"},
    {"value": "ANGULAR", "label": "Angular"},
    {"value": "REACT", "label": "React"},
    {"value": "AGENTIC_AI", "label": "Agentic AI"},
    {"value": "SOFT_SKILL", "label": "Soft Skill"},
    {"value": "NODE", "label": "Node"},
    {"value": "TESTING", "label": "Testing"},
    {"value": "DEVOPS", "label": "DevOps"},
]

MEDICINE_CATEGORIES = {"AYURVEDIC", "ALLOPATHIC", "HOMEOPATHIC", "OTHER"}


def parse_json_part(value):
    if value is None:
        return {}
    if hasattr(value, "read"):
        raw_value = value.read().decode("utf-8")
    else:
        raw_value = str(value)
    return json.loads(raw_value)


def file_suffix(uploaded_file) -> str:
    return Path(uploaded_file.name).suffix if uploaded_file and uploaded_file.name else ""