import requests
from typing import List
from ..job_models import Job, detect_skills

API_URL = "https://remotive.com/api/remote-jobs"


def search_remotive(query: str) -> List[Job]:
    try:
        params = {"search": query}
        r = requests.get(API_URL, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        jobs: List[Job] = []
        for item in data.get("jobs", []):
            title = item.get("title", "")
            company = item.get("company_name", "")
            url = item.get("url", "")
            desc = item.get("description", "")
            loc = item.get("candidate_required_location") or item.get("job_type")
            skills = detect_skills(" ".join([title, company, desc, loc or ""]), query)
            jobs.append(Job(
                title=title,
                company=company,
                description=desc,
                skills=skills,
                url=url,
                source="Remotive",
                location_hint=loc,
            ))
        return jobs
    except Exception:
        return []
