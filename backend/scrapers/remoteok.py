import requests
from bs4 import BeautifulSoup
from typing import List
from ..job_models import Job, detect_skills

BASE_URL = "https://remoteok.com/"


def search_remoteok(query: str) -> List[Job]:
    try:
        # RemoteOK HTML is simple; also has JSON, but HTML parsing avoids API limits.
        url = f"{BASE_URL}remote-{query.replace(' ', '-')}-jobs"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        jobs: List[Job] = []
        for row in soup.select("tr.job"):  # job rows
            title_el = row.select_one("h2")
            company_el = row.select_one("h3")
            link_el = row.get("data-href")
            if not title_el or not company_el or not link_el:
                continue
            title = title_el.get_text(strip=True)
            company = company_el.get_text(strip=True)
            url = BASE_URL.rstrip("/") + link_el
            desc = " ".join(t.get_text(" ", strip=True) for t in row.select("div.description, td.tags"))
            loc = row.select_one("div.location, td.location")
            loc_text = loc.get_text(" ", strip=True) if loc else None
            skills = detect_skills(" ".join([title, company, desc, loc_text or ""]), query)
            jobs.append(Job(
                title=title,
                company=company,
                description=desc,
                skills=skills,
                url=url,
                source="RemoteOK",
                location_hint=loc_text,
            ))
        return jobs
    except Exception:
        return []
