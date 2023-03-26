import pytest
from src import convert_jobs_to_df
from src import JobsData
import polars as pl


@pytest.fixture(autouse=True)
def mock_jobs_data():
    jobs = JobsData(
        date=[],
        keyword=[],
        city=[],
        jobs_qty=[]
    )

    df = pl.read_parquet('./tests/fixtures/jobs_mock_df.parquet')
    df.schema
    df = df.with_columns(
        pl.col('city').cast(pl.Utf8),
        pl.col("keyword").cast(pl.Utf8),
        pl.col('jobs_qty').cast(pl.Utf8)
    )
    jobs.date = df.get_column('date').to_list()
    jobs.keyword = df.get_column("keyword").to_list()
    jobs.city = df.get_column("city").to_list()
    jobs.jobs_qty = df.get_column("jobs_qty").to_list()

    return jobs

def test_convert_jobs_to_df(mock_jobs_data):
    df = convert_jobs_to_df(mock_jobs_data)
    assert isinstance(df, pl.DataFrame)
    

