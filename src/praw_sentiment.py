import os
import praw
import polars as pl
from dotenv import load_dotenv
from datetime import datetime, timezone
from src.classes import SubmissionsData, CommentsData
from dataclasses import asdict

load_dotenv()

# TODO Add logger
# Add tests

submission_data = SubmissionsData()
comment_data = CommentsData()

reddit = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    user_agent=os.environ.get("USER_AGENT"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD"),
)


subreddit_names = {
    "London": "lontonontario",
    "Kitcher / Waterloo": "waterloo+Kitchener",
    "Toronto": "toronto",
    "Mississauga": "mississauga",
    "Calgary": "calgary",
    "Hamilton": "Hamilton",
    "Windsor": "windsorontario",
    "Ottawa": "ottawa",
}


def save_comment(submission, comment, parent_id=None):
    if parent_id:
        comment_data.reply_id.append(parent_id)
    else:
        comment_data.reply_id.append("")

    comment_date_utc = datetime.fromtimestamp(comment.created_utc, timezone.utc)

    comment_data.submission_id.append(submission.id)
    comment_data.date.append(comment_date_utc)
    comment_data.comment.append(comment.body)
    comment_data.is_author.append(comment.is_submitter)
    comment_data.is_distinguished.append(comment.distinguished)


def convert_submissions_to_df(submission):
    df = pl.DataFrame(asdict(submission))
    assert df.columns == ["date_utc", "keyword", "city", "jobs_qty"]
    df = df.with_columns(
        pl.col("date_utc").cast(pl.Date),
        pl.col("keyword").cast(pl.Utf8),
        pl.col("city").cast(pl.Utf8),
        pl.col("jobs_qty").str.replace(",", "").cast(pl.Int64),
    )

    return df


for sub_name, keyword in subreddit_names.items():
    subreddit = reddit.subreddit(keyword)
    latest_submissions = subreddit.top(limit=5, time_filter="week")
    for submission in latest_submissions:
        date_utc = datetime.fromtimestamp(submission.created_utc, timezone.utc)

        submission_data.submission_id.append(submission.id)
        submission_data.date.append(date_utc)
        submission_data.subreddit.append(sub_name)
        submission_data.title.append(submission.title)
        submission.name
        submission_data.upvote_ratio.append(submission.upvote_ratio)

        if submission.num_comments > 0:
            for comment in submission.comments:
                save_comment(submission, comment)

                if len(comment.replies) > 0:
                    for reply in comment.replies:
                        save_comment(submission, reply, reply.id)
