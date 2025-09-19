from typing import List, Protocol
from ..job_models import Job

class Scraper(Protocol):
    def __call__(self, query: str) -> List[Job]:
        ...
