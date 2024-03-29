import os
import praw
import sys
import polars as pl
from typing import Literal
from dataclasses import asdict
from datetime import datetime, timezone
from src.classes import SubmissionsData, CommentsData


# TODO Add logger and change prints for logs. Make sure that the logs persist on azure file share with a volume.
# Add tests

submission_data = SubmissionsData()
comment_data = CommentsData()

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD"),
)


subreddit_names = {
    "London": "londonontario",
    "Kitcher / Waterloo": "waterloo+Kitchener",
    "Toronto": "toronto",
    "Mississauga": "mississauga",
    "Calgary": "calgary",
    "Hamilton": "Hamilton",
    "Windsor": "windsorontario",
    "Ottawa": "ottawa",
}


def save_comment(submission, comment, parent_id: bool = False):
    try:
        if comment.distinguished:
            comment_data.is_moderator.append(True)
        else:
            comment_data.is_moderator.append(False)
        comment_date_utc = datetime.fromtimestamp(comment.created_utc, timezone.utc)
        comment_data.submission_id.append(submission.id)
        comment_data.comment_id.append(comment.id)
        comment_data.date_utc.append(comment_date_utc)
        comment_data.comment.append(comment.body)
        comment_data.is_author.append(comment.is_submitter)
        comment_data.score.append(comment.score)
        if parent_id:
            tier, parent_id = comment.parent_id.split("_")

            comment_data.parent_id.append(parent_id)
            comment_data.comment_tier.append(tier)
        else:
            comment_data.parent_id.append("")
            comment_data.comment_tier.append("")
    except Exception as e:
        print(
            "Comment exception found: ",
            e,
            f"skipping comment id {comment.id} from submission {submission.id}...",
        )


def convert_submissions_to_df(submission_data: SubmissionsData):
    df = pl.DataFrame(asdict(submission_data))
    assert df.columns == [
        "submission_id",
        "subreddit",
        "date_utc",
        "title",
        "upvote_ratio",
    ]
    df = df.with_columns(
        pl.col("submission_id").cast(pl.Utf8),
        pl.col("subreddit").cast(pl.Utf8),
        pl.col("date_utc").cast(pl.Date),
        pl.col("title").cast(pl.Utf8),
        pl.col("upvote_ratio").cast(pl.Float32),
    )

    return df


def convert_comments_to_df(comment_data):
    df = pl.DataFrame(asdict(comment_data))
    assert df.columns == [
        "submission_id",
        "comment_id",
        "comment_tier",
        "parent_id",
        "date_utc",
        "comment",
        "is_moderator",
        "is_author",
        "score",
    ]
    df = df.with_columns(
        pl.col("submission_id").cast(pl.Utf8),
        pl.col("comment_id").cast(pl.Utf8),
        pl.col("comment_tier").cast(pl.Utf8),
        pl.col("parent_id").cast(pl.Utf8),
        pl.col("date_utc").cast(pl.Date),
        pl.col("comment").cast(pl.Utf8),
        pl.col("is_moderator").cast(pl.Boolean),
        pl.col("is_author").cast(pl.Boolean),
        pl.col("score").cast(pl.Int64),
    )

    return df


def get_reddit_submissions_with_comments(
    number_of_submissions: int, period: Literal["day", "month"]
):
    for sub_name, keyword in subreddit_names.items():
        print(f"Gathering data from: {sub_name}")
        subreddit = reddit.subreddit(keyword)
        latest_submissions = subreddit.top(
            limit=number_of_submissions, time_filter=period
        )

        try:
            next(latest_submissions)
        except Exception as e:
            print(f"Subreddit not found {sub_name}: {e}")
            sys.exit(0)

        for submission in latest_submissions:
            date_utc = datetime.fromtimestamp(submission.created_utc, timezone.utc)

            submission_data.submission_id.append(submission.id)
            submission_data.date_utc.append(date_utc)
            submission_data.subreddit.append(sub_name)
            submission_data.title.append(submission.title)
            submission_data.upvote_ratio.append(submission.upvote_ratio)

            if submission.num_comments > 0:
                for comment in submission.comments:
                    save_comment(submission, comment)

                    try:
                        for reply in comment.replies:
                            save_comment(submission, reply, True)
                    except Exception as e:
                        print(f"Comment {comment.id} from {submission} has no replies.")

    submissions_df = convert_submissions_to_df(submission_data)
    comments_df = convert_comments_to_df(comment_data)

    return submissions_df, comments_df


if __name__ == "__main__":
    get_reddit_submissions_with_comments()
