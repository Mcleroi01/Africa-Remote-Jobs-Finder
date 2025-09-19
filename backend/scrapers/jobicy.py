import requests
from bs4 import BeautifulSoup
from typing import List
from ..job_models import Job, detect_skills

BASE_URL = "https://jobicy.com/search/?q="


def search_jobicy(query: str) -> List[Job]:
    try:
        url = f"{BASE_URL}{requests.utils.quote(query)}&remote=1"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        jobs: List[Job] = []
        for li in soup.select("ul.jobs-list li"):
            a = li.select_one("h3 a") or li.select_one("a")
            if not a:
                continue
            title = a.get_text(strip=True)
            link = a.get("href")
            company_el = li.select_one("div.company, span.company")
            company = company_el.get_text(strip=True) if company_el else ""
            desc_el = li.select_one("div.job-list-item, p")
            desc = desc_el.get_text(" ", strip=True) if desc_el else ""
            loc_el = li.select_one("span.region, span.location")
            loc = loc_el.get_text(strip=True) if loc_el else None
            skills = detect_skills(" ".join([title, company, desc, loc or ""]), query)
            jobs.append(Job(
                title=title,
                company=company,
                description=desc,
                skills=skills,
                url=link or "",
                source="Jobicy",
                location_hint=loc,
            ))
        return jobs
    except Exception:
        return []
