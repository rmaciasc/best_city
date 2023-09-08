import polars as pl
from time import sleep
from bs4 import BeautifulSoup
from dataclasses import asdict
from selenium import webdriver
from src.classes import JobsData
from src.utils.logs import logger
from datetime import datetime, timezone
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


state = {
    "search_keywords": ["Data", "Python"],
    "cities": ["London", "Kitchener", "Toronto", "Ottawa", "Calgary"],
}

BASE_URL = "https://www.workopolis.com/jobsearch/find-jobs?ak=[[KEYWORD]]&l=[[CITY]]"


def retrieve_jobs():
    jobs = JobsData()
    driver = get_chromedriver()

    for keywords in state["search_keywords"]:
        for city in state["cities"]:
            logger.info(f"Retrieving jobs for the keywords {keywords.upper()} in {city.upper()}")
            url = BASE_URL.replace("[[KEYWORD]]", keywords.replace(" ", "+")).replace("[[CITY]]", city)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
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


def get_chromedriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


if __name__ == "__main__":
    jobs = retrieve_jobs()
    df = convert_jobs_to_df(jobs)
    test_jobs_df(df)
