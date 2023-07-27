from src.utils.df_saver import upload_df
from datetime import datetime
from src.utils.logs import logger
from src.jobs import retrieve_jobs, convert_jobs_to_df, test_jobs_df
from src.praw_sentiment import get_reddit_submissions_with_comments


logger.info("Getting submissions with comments...")
submissions_df, comments_df = get_reddit_submissions_with_comments(7, "day")
logger.info("Uploading submissions with comments...")
upload_df(submissions_df, f"submissions_{datetime.now().date()}", mode="parquet")
upload_df(comments_df, f"comments_{datetime.now().date()}", mode="parquet")
logger.info("Submissions with comments are successfully saved...")

logger.info("Getting number of jobs...")
jobs = retrieve_jobs()
jobs_df = convert_jobs_to_df(jobs)
test_jobs_df(jobs_df)

upload_df(jobs_df, f"jobs_{datetime.now().date()}", mode="parquet")
