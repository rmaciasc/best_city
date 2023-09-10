from src.utils.df_saver import postgres_db, azure_storage
from datetime import datetime
from src.utils.logs import logger
from src.jobs import retrieve_jobs, convert_jobs_to_df, test_jobs_df
from src.praw_sentiment import get_reddit_submissions_with_comments


def main():
    weekday = datetime.now().weekday()
    storage = postgres_db()

    logger.info("Getting submissions with comments...")
    submissions_df, comments_df = get_reddit_submissions_with_comments(7, "day")
    logger.info("Uploading submissions with comments...")
    storage.save_df(submissions_df, "submissions")
    storage.save_df(comments_df, "comments")
    logger.info("Submissions with comments are successfully saved...")

    if weekday == 6:
        logger.info("Getting number of jobs...")
        jobs = retrieve_jobs()
        jobs_df = convert_jobs_to_df(jobs)
        test_jobs_df(jobs_df)

        storage.save_df(jobs_df, "jobs")


if __name__ == "__main__":
    main()
