from src.utils.df_saver import upload_df
from datetime import datetime
from src.utils.logs import logger
from src.jobs import retrieve_jobs, convert_jobs_to_df, test_jobs_df
from src.praw_sentiment import get_reddit_submissions_with_comments


def main():
    weekday = datetime.now().weekday()
    container_name = "best-city"

    logger.info("Getting submissions with comments...")
    submissions_df, comments_df = get_reddit_submissions_with_comments(7, "day")
    logger.info("Uploading submissions with comments...")
    upload_df(submissions_df, f"submissions/submissions_{datetime.now().date()}", container_name, mode="parquet")
    upload_df(comments_df, f"comments/comments_{datetime.now().date()}", container_name, mode="parquet")
    logger.info("Submissions with comments are successfully saved...")

    if weekday == 6:
        logger.info("Getting number of jobs...")
        jobs = retrieve_jobs()
        jobs_df = convert_jobs_to_df(jobs)
        test_jobs_df(jobs_df)

        upload_df(jobs_df, f"jobs/jobs_{datetime.now().date()}", container_name, mode="parquet")


if __name__ == "__main__":
    main()
