from src.praw_sentiment import get_reddit_submissions_with_comments
from src.jobs import retrieve_jobs, convert_jobs_to_df, test_jobs_df
from src.utils.logs import logger

submissions_df, comments_df = get_reddit_submissions_with_comments(7, "day")

logger.info("Getting number of jobs...")
jobs = retrieve_jobs()
jobs_df = convert_jobs_to_df(jobs)
test_jobs_df(jobs_df)


print(submissions_df)
print(comments_df)
print(jobs_df)
