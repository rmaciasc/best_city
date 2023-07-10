from datetime import datetime
from dataclasses import dataclass, field


@dataclass(slots=True)
class JobsData:
    """Dataclass to hold jobs data
    Args:
        date_utc (list[datetime.date]): Date of the job search.
        keyword (list[str]): Keyword of the job search.
        city (list[str]): City of the job search.
        jobs_qty (list[str]): Amount of results in the job search.
    """

    date_utc: list[datetime.date] = field(default_factory=list)
    keyword: list[str] = field(default_factory=list)
    city: list[str] = field(default_factory=list)
    jobs_qty: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SubmissionsData:
    """Dataclass to hold Reddit submissions data
    Args:
        submission_id (list[str])
        subreddit (list[str]): Name of the subreddit.
        date_utc (list[datetime.date]): Creation date of the submission in UTC.
        title (list[str]): Title of the submission.
        upvote_ratio (list[str]): Upvote ratio of the submission.
    """

    submission_id: list[str] = field(default_factory=list)
    subreddit: list[str] = field(default_factory=list)
    date_utc: list[datetime] = field(default_factory=list)
    title: list[str] = field(default_factory=list)
    upvote_ratio: list[float] = field(default_factory=list)


@dataclass(slots=True)
class CommentsData:
    """Dataclass to hold Reddit comments data for each subreddit
    Args:
        submission_id (list[str]): Id of the parent submission.
        reply_id (list[str]): Id of the parent comment if applicable.
        date_utc (list[datetime.date]): Creation date of the submission in UTC.
        comment (list[str]): Comment of the submission.
        is_moderator (list[str])
        is_author (list[str])
    """

    submission_id: list[str] = field(default_factory=list)
    reply_id: list[str] = field(default_factory=list)
    date_utc: list[datetime] = field(default_factory=list)
    comment: list[str] = field(default_factory=list)
    is_moderator: list[bool] = field(default_factory=list)
    is_author: list[bool] = field(default_factory=list)
