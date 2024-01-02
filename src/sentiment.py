import os
import psycopg2
import numpy as np
import polars as pl
from tqdm import tqdm
from typing import Union
from typing import Literal
from dotenv import load_dotenv
from scipy.special import softmax
from src.bad_words_detector import detect_bad_words
from transformers import (
    AutoTokenizer,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    RobertaForSequenceClassification,
)

load_dotenv()


def read_from_database():
    conn_uri: str = os.environ["POSTGRES_CONN_URI"]
    conn = psycopg2.connect(conn_uri)
    query = """SELECT * FROM raw.submissions rc
                WHERE NOT EXISTS (
                    SELECT * FROM staging.submissions
                    WHERE submission_id = rc.submission_id
                );"""
    query_comm = """SELECT * FROM raw.comments rc
                    WHERE NOT EXISTS (
                        SELECT * FROM staging.comments
                        WHERE comment_id = rc.comment_id
                    );"""
    df_comm = pl.read_database(query_comm, conn)
    df_sub = pl.read_database(query, conn)
    return df_comm, df_sub


def load_model():
    pretrained: str = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(pretrained)

    model = RobertaForSequenceClassification.from_pretrained(pretrained)
    return model, tokenizer


def get_sentiment(text, model, tokenizer) -> np.ndarray:
    """Returns a ndarray with three items:
    - First item contains the score for a negative sentiment
    - Second item contains the score for a neutral sentiment
    - Third item contains the score for a positive sentiment
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    output = model(**inputs)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores


def get_weighted_sentiment_score(
    text: str,
    model: RobertaForSequenceClassification,
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
    weights=[-1, 0, 1],
) -> np.float64:
    scores: np.ndarray = get_sentiment(text, model, tokenizer)
    return round(np.dot(scores, weights), 5)


def w_pbar(pbar, func):
    def foo(*args, **kwargs):
        pbar.update(1)
        return func(*args, **kwargs)

    return foo


def add_sentiment(
    df: pl.DataFrame,
    tbl_name: Literal["comment", "submission"],
    model: RobertaForSequenceClassification,
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
):
    if df.is_empty():
        print(f"{tbl_name.capitalize()} dataframe is empty, skiping...")
        return df
    pbar = tqdm(total=len(df), desc="Adding sentiment column", colour="green")
    tbl_name = "title" if tbl_name == "submission" else tbl_name
    ## Add sentiment
    df = df.with_columns(
        pl.col(tbl_name)
        .map_elements(
            w_pbar(pbar, lambda x: get_weighted_sentiment_score(x, model, tokenizer))
        )
        .alias(f"{tbl_name}_sentiment")
    )
    pbar.close()
    return df


def add_bad_words(df: pl.DataFrame):
    pbar = tqdm(total=len(df), desc="Adding bad words column", colour="green")
    df = df.with_columns(
        bad_words=pl.col("comment").map_elements(
            w_pbar(pbar, lambda x: detect_bad_words(x))
        )
    )
    pbar.close()
    return df


def remove_moderators_comments_df(df):
    ## Remove comments from moderators
    df = df.filter(pl.col("is_moderator") != True)
    df = df.drop("is_moderator")
    return df
