import requests
from typing import List
from ..job_models import Job, detect_skills

# Selected AI/Dev companies using Greenhouse boards
GREENHOUSE_COMPANIES = [
    ("OpenAI", "openai"),
    ("Anthropic", "anthropic"),
    ("Cohere", "cohere"),
    ("Stability AI", "stabilityai"),
    ("Hugging Face", "huggingface"),
    ("GitHub", "github"),
]

API_TMPL = "https://boards-api.greenhouse.io/v1/boards/{board}/jobs"


def search_ai_companies(query: str) -> List[Job]:
    q = (query or "").lower()
    headers = {"User-Agent": "Mozilla/5.0"}
    jobs: List[Job] = []
    for company_name, board in GREENHOUSE_COMPANIES:
        try:
            url = API_TMPL.format(board=board)
            r = requests.get(url, headers=headers, timeout=20)
            r.raise_for_status()
            data = r.json()
            for item in data.get("jobs", []):
                title = item.get("title", "")
                loc = (item.get("location") or {}).get("name") if item.get("location") else None
                abs_url = item.get("absolute_url", "")
                # basic text to match and eligibility hints
                desc = " ".join([dept.get("name", "") for dept in item.get("departments", [])])
                text = " ".join([title, company_name, desc or "", loc or ""]).lower()
                if q and q not in text:
                    continue
                skills = detect_skills(" ".join([title, company_name, desc, loc or ""]), query)
                jobs.append(Job(
                    title=title,
                    company=company_name,
                    description=desc,
                    skills=skills,
                    url=abs_url,
                    source="AI Companies (Greenhouse)",
                    location_hint=loc,
                ))
        except Exception:
            continue
    return jobs
