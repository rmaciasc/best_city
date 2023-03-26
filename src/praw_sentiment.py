import os
import praw
from dotenv import load_dotenv

load_dotenv()


reddit = praw.Reddit(
    client_id = os.environ.get("CLIENT_ID"),
    client_secret = os.environ.get("CLIENT_SECRET"),
    user_agent=os.environ.get("USER_AGENT"), 
    username=os.environ.get("REDDIT_USERNAME"), 
    password=os.environ.get("REDDIT_PASSWORD"),
    )

london_on = reddit.subreddit('londonontario')

latest_posts = london_on.new(limit = 10)

for post in latest_posts:
    post.title