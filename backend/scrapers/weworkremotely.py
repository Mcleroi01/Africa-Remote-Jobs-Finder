import requests
from bs4 import BeautifulSoup
from typing import List
from ..job_models import Job, detect_skills

BASE_URL = "https://weworkremotely.com/"


def search_wwr(query: str) -> List[Job]:
    try:
        url = f"{BASE_URL}remote-jobs/search?term={requests.utils.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        jobs: List[Job] = []
        for li in soup.select("section.jobs li.feature, section.jobs li:not(.view-all)"):
            a = li.select_one("a[href^='/remote-jobs']")
            if not a:
                continue
            title_el = li.select_one("span.title")
            company_el = li.select_one("span.company")
            if not title_el or not company_el:
                continue
            title = title_el.get_text(strip=True)
            company = company_el.get_text(strip=True)
            link = a.get("href")
            url = BASE_URL.rstrip("/") + link
            # Fetch job page for more details
            try:
                jr = requests.get(url, headers=headers, timeout=20)
                jr.raise_for_status()
                jsoup = BeautifulSoup(jr.text, "lxml")
                desc = jsoup.select_one("div.listing-container").get_text(" ", strip=True) if jsoup.select_one("div.listing-container") else ""
                loc = None
                loc_el = jsoup.select_one("div.location");
                if loc_el:
                    loc = loc_el.get_text(" ", strip=True)
            except Exception:
                desc = ""
                loc = None
            skills = detect_skills(" ".join([title, company, desc, loc or ""]), query)
            jobs.append(Job(
                title=title,
                company=company,
                description=desc,
                skills=skills,
                url=url,
                source="WeWorkRemotely",
                location_hint=loc,
            ))
        return jobs
    except Exception:
        return []
