import os
import praw
from dotenv import load_dotenv
from datetime import datetime, timezone
from src.dataclasses import SubmissionsData

load_dotenv()

# TODO Add logger
# Add tests

sub_data = SubmissionsData()

reddit = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    user_agent=os.environ.get("USER_AGENT"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD"),
)

subreddits = [
    "lontonontario",
    "waterloo+Kitchener",
    # "toronto",
    # "mississauga",
    # "calgary",
    # "Hamiltonontario",
    # "asdffsdaasdf",
    # "asdffsdaasdf",
    # "asdffsdaasdf",
]

subreddits = {
    "London": "lontonontario",
    "Kitcher / Waterloo": "waterloo+Kitchener",
    # "Toronto": "toronto",
    # "Mississauga": "mississauga",
    # "Calgary": "calgary",
    # "Hamilton": "Hamiltonontario",
    # "asdffsdaasdf",
    # "asdffsdaasdf",
    # "asdffsdaasdf",
}

for subreddit in subreddits:
    subreddit
    latest_submissions = subreddit.top(limit=5, time_filter="week")
    for submission in latest_submissions:
        submission.title
        date_utc = datetime.fromtimestamp(submission.created_utc, timezone.utc)
        submission.upvote_ratio
        for comment in submission.comments:
            comment.body
            if len(comment.replies) > 0:
                for i in range(0, len(comment.replies)):
                    print(f"**********{comment.replies[i].body}")
