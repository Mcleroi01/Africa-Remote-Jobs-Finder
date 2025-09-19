from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable
from .job_models import Job, filter_jobs
from .scrapers.remoteok import search_remoteok
from .scrapers.weworkremotely import search_wwr
from .scrapers.remotive import search_remotive
from .scrapers.remote_co import search_remote_co
from .scrapers.jobicy import search_jobicy
from .scrapers.ai_companies import search_ai_companies


SCRAPERS: Dict[str, Callable[[str], List[Job]]] = {
    "RemoteOK": search_remoteok,
    "WeWorkRemotely": search_wwr,
    "Remotive": search_remotive,
    "Remote.co": search_remote_co,
    "Jobicy": search_jobicy,
    "AI Companies (Greenhouse)": search_ai_companies,
}


def available_sources() -> List[str]:
    return list(SCRAPERS.keys())


def search_all(query: str, sources: List[str] | None = None) -> List[Job]:
    selected = sources or available_sources()
    fns = [SCRAPERS[name] for name in selected if name in SCRAPERS]
    # Run scrapers concurrently
    with ThreadPoolExecutor(max_workers=min(6, len(fns) or 1)) as ex:
        futures = [ex.submit(fn, query) for fn in fns]
        jobs: List[Job] = []
        for f in futures:
            try:
                jobs.extend(f.result() or [])
            except Exception:
                pass
    return filter_jobs(jobs)
