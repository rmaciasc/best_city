import requests
import polars as pl
from time import sleep
from datetime import datetime, timezone
from src.utils.logs import logger
from bs4 import BeautifulSoup
from dataclasses import asdict
from src.classes import JobsData

state = {
    "search_keywords": ["Data", "Python"],
    "cities": ["London", "Kitchener", "Toronto", "Ottawa"],
}

HEADERS = {
    "authority": "d3fw5vlhllyvee.cloudfront.net",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://www.workopolis.com",
    "pragma": "no-cache",
    "referer": "https://www.workopolis.com/",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
}

BASE_URL = "https://www.workopolis.com/jobsearch/find-jobs?ak=[[KEYWORD]]&l=[[CITY]]"


def get_job_soup(keywords: str, city: str) -> BeautifulSoup | None:
    url = BASE_URL.replace("[[KEYWORD]]", keywords.replace(" ", "+")).replace("[[CITY]]", city)

    result = requests.get(url, headers=HEADERS)

    # check HTTP response status codes to find if HTTP request has been successfully completed
    if result.status_code >= 100 and result.status_code <= 199:
        logger.error("Informational response")
    if result.status_code >= 200 and result.status_code <= 299:
        logger.debug("Successful response")
        return BeautifulSoup(result.content, "lxml")
    if result.status_code >= 300 and result.status_code <= 399:
        logger.warning("Redirect")
    if result.status_code >= 400 and result.status_code <= 499:
        logger.error("Client error")
    if result.status_code >= 500 and result.status_code <= 599:
        logger.error("Server error")


def retrieve_jobs():
    jobs = JobsData()

    for keywords in state["search_keywords"]:
        for city in state["cities"]:
            logger.info(f"Retrieving jobs for the keywords {keywords.upper()} in {city.upper()}")
            soup = get_job_soup(keywords, city)
            res = soup.select("div #job-list")
            count_jobs_found = res[0]["aria-label"].split(" ")[0]

            jobs.date_utc.append(datetime.now(timezone.utc).date())
            jobs.city.append(city)
            jobs.keyword.append(keywords)
            jobs.jobs_qty.append(count_jobs_found)
            sleep(5)

    return jobs


def convert_jobs_to_df(jobs):
    df = pl.DataFrame(asdict(jobs))
    assert df.columns == ["date_utc", "keyword", "city", "jobs_qty"]
    df = df.with_columns(
        pl.col("date_utc").cast(pl.Date),
        pl.col("city").cast(pl.Utf8),
        pl.col("keyword").cast(pl.Utf8),
        pl.col("jobs_qty").str.replace(",", "").cast(pl.Int64),
    )

    return df


def test_jobs_df(df: pl.DataFrame):
    assert isinstance(df, pl.DataFrame)
    assert df.is_empty() is False, "Dataframe is empty."
    ## Check for nulls
    assert df.select([pl.any(pl.all().is_null())]).sum()[0, 0] == 0, "NULL values found in Dataframe."
    ## Check for empty str
    assert df.select(pl.col(pl.Utf8) == "").sum().sum(axis=1)[0] == 0, "Empty str found in Dataframe."
    ## Check for str with spaces
    assert df.select(pl.col(pl.Utf8) == " ").sum().sum(axis=1)[0] == 0, "Blank str found in Dataframe"


if __name__ == "__main__":
    logger.info("Getting number of jobs...")
    jobs = retrieve_jobs()
    df = convert_jobs_to_df(jobs)
    test_jobs_df(df)
