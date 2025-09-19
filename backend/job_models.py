from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import re


AFRICA_KEYWORDS = [
    "africa", "nigeria", "ghana", "kenya", "senegal", "morocco", "egypt", "south africa",
    "cameroon", "ivory coast", "cote d'ivoire", "ethiopia", "tanzania", "uganda", "rwanda",
    "algeria", "tunisia", "botswana", "namibia", "zimbabwe", "mozambique", "angola"
]

GLOBAL_REMOTE_KEYWORDS = [
    "global", "worldwide", "anywhere", "international", "remote international", "remote (anywhere)",
    "open to anywhere", "work from anywhere"
]

REMOTE_KEYWORDS = ["remote", "work from home", "distributed", "async"]


@dataclass
class Job:
    title: str
    company: str
    description: str
    skills: List[str]
    url: str
    source: str
    location_hint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def detect_skills(text: str, query: str) -> List[str]:
    # extract keyword and common stacks in the text
    stacks = [
        "python", "django", "flask", "fastapi",
        "javascript", "typescript", "react", "next.js", "vue", "nuxt",
        "node", "express",
        "java", "spring",
        "kotlin", "android",
        "swift", "ios",
        "flutter", "dart",
        "laravel", "php",
        "ruby", "rails",
        "go", "golang",
        "rust",
        "aws", "gcp", "azure",
        "postgres", "mysql", "mongodb",
        "docker", "kubernetes",
        "fullstack", "frontend", "backend",
    ]
    terms = set()
    q = query.strip().lower()
    if q:
        terms.add(q)
    lower = text.lower()
    for s in stacks:
        if re.search(r"\b" + re.escape(s) + r"\b", lower):
            terms.add(s)
    return sorted(list(terms))[:5]


def looks_remote(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in REMOTE_KEYWORDS)


def africa_friendly(text: str) -> bool:
    t = text.lower()
    if any(k in t for k in GLOBAL_REMOTE_KEYWORDS):
        return True
    if any(k in t for k in AFRICA_KEYWORDS):
        return True
    # Explicit exclusions (US only, EU only, timezone hard limits with strong exclusions)
    exclusions = [
        "us only", "europe only", "eu only", "must be in us", "canada only",
        "no international", "not international", "no remote outside"
    ]
    if any(x in t for x in exclusions):
        return False
    # timezone hints: allow EMEA, GMT to GMT+3 etc.
    allow_hints = ["emea", "gmt", "utc", "bst", "west africa", "central africa", "east africa"]
    if any(h in t for h in allow_hints):
        return True
    return False


def filter_jobs(jobs: List[Job]) -> List[Job]:
    seen = set()
    filtered = []
    for j in jobs:
        key = (j.title.lower().strip(), j.company.lower().strip())
        if key in seen:
            continue
        seen.add(key)
        text = " ".join([j.title, j.company, j.description or "", j.location_hint or ""]).lower()
        if looks_remote(text) and africa_friendly(text):
            filtered.append(j)
    return filtered
