import io
import os
import polars as pl
from typing import Literal
from polars import DataFrame
from dotenv import load_dotenv
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential

load_dotenv()

storage_url = os.environ["AZURE_STORAGE_BLOB_URL"]
credential = DefaultAzureCredential()

df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "groups": ["A", "A", "B", "C", "B"],
    }
)
print(df)

file_name = "test/test"
container_name = "best-city"
mode = "csv"


def upload_df(df: DataFrame, file_name: str, container_name: str, mode: Literal["csv", "parquet"]) -> None:
    b_buf = io.BytesIO()
    if mode == "parquet":
        df.write_parquet(b_buf)
    if mode == "csv":
        df.write_csv(b_buf)
    b_buf.seek(0)

    container_client = ContainerClient(account_url=storage_url, container_name=container_name, credential=credential)
    container_client.upload_blob(f"{file_name}.{mode}", b_buf, overwrite=True)
