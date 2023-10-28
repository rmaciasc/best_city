from src.sentiment import load_model, read_from_database, add_bad_words, add_sentiment, remove_moderators_comments_df
from src.utils.df_saver import postgres_db


def main():
    storage = postgres_db()

    model, tokenizer = load_model()
    tokenizer.model_max_length = 512
    df_comm, df_sub = read_from_database()

    df_sub = add_sentiment(df_sub, "submission", model, tokenizer)

    df_comm = remove_moderators_comments_df(df_comm)
    df_comm = add_sentiment(df_comm, "comment", model, tokenizer)
    df_comm = add_bad_words(df_comm)

    storage.save_df(df_sub, "staging", "submissions")
    storage.save_df(df_comm, "staging", "comments")


if __name__ == "__main__":
    main()
