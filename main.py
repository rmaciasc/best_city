from src.praw_sentiment import get_reddit_submissions_with_comments

submissions_df, comments_df = get_reddit_submissions_with_comments(7, "day")

print(submissions_df)
print(comments_df)
