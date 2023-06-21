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


@dataclass
class SubmissionsData:
    """Dataclass to hold Reddit submissions data
    Args:
        date_utc (list[datetime.date]): Creation date of the submission in UTC.
        title (list[str]): Title of the submission.
        upvote_ratio (list[str]): Upvote ratio of the submission.
        comments (list[str]): Comments in the submission.
    """

    date: list[datetime]
    subreddit: list[str]
    title: list[str]
    upvote_ratio: list[float]
