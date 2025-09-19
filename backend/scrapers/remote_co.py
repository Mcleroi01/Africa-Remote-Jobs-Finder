import requests
from bs4 import BeautifulSoup
from typing import List
from ..job_models import Job, detect_skills

BASE_URL = "https://remote.co/remote-jobs/search/?search_keywords="


def search_remote_co(query: str) -> List[Job]:
    try:
        url = f"{BASE_URL}{requests.utils.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        jobs: List[Job] = []
        for card in soup.select("li.card, article.card"):  # layout may vary
            a = card.select_one("a.card-title, a:text") or card.select_one("a")
            if not a:
                continue
            title = a.get_text(strip=True)
            link = a.get("href")
            if link and link.startswith("/"):
                link = "https://remote.co" + link
            company_el = card.select_one("span.company, div.company, p.company")
            company = company_el.get_text(strip=True) if company_el else ""
            desc_el = card.select_one("div.card-body, p")
            desc = desc_el.get_text(" ", strip=True) if desc_el else ""
            loc_el = card.select_one("span.location, div.location")
            loc = loc_el.get_text(strip=True) if loc_el else None
            skills = detect_skills(" ".join([title, company, desc, loc or ""]), query)
            jobs.append(Job(
                title=title,
                company=company,
                description=desc,
                skills=skills,
                url=link or "",
                source="Remote.co",
                location_hint=loc,
            ))
        return jobs
    except Exception:
        return []
