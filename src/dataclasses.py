from datetime import datetime
from dataclasses import dataclass

@dataclass
class JobsData:
    """Dataclass to hold jobs data
    Args:
        date (list[datetime.date]): Date of the job search.
        keyword (list[str]): Keyword of the job search.
        city (list[str]): City of the job search.
        jobs_qty (list[str]): Amount of results in the job search.
    """
    date: list[datetime.date]
    keyword: list[str]
    city: list[str]
    jobs_qty: list[str]