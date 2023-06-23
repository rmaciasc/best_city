import os
import praw
from dotenv import load_dotenv
from datetime import datetime, timezone
from src.classes import SubmissionsData

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


subreddit_names = {
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

for sub_name, keyword in subreddit_names.items():
    sub_name
    keyword
    subreddit = reddit.subreddit(keyword)
    latest_submissions = subreddit.top(limit=5, time_filter="week")
    for submission in latest_submissions:
        date_utc = datetime.fromtimestamp(submission.created_utc, timezone.utc)

        sub_data.date.append(date_utc)
        sub_data.subreddit.append(sub_name)
        sub_data.title.append(submission.title)
        sub_data.upvote_ratio.append(submission.upvote_ratio)

        for comment in submission.comments:
            comment.body
            if len(comment.replies) > 0:
                for i in range(0, len(comment.replies)):
                    print(f"**********{comment.replies[i].body}")
