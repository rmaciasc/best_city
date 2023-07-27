import io
import os
from typing import Literal
from polars import DataFrame
from dotenv import load_dotenv
from azure.storage.blob import ContainerClient

load_dotenv()

CONN_STRING = os.environ.get("AZURE_CONN_STRING")


def upload_df(df: DataFrame, file_name: str, container_name: str, mode: Literal["csv", "parquet"]) -> None:
    b_buf = io.BytesIO()
    if mode == "parquet":
        df.write_parquet(b_buf)
    if mode == "csv":
        df.write_csv(b_buf)
    b_buf.seek(0)

    container_client = ContainerClient.from_connection_string(CONN_STRING, container_name)
    container_client.upload_blob(f"{file_name}.{mode}", b_buf, overwrite=True)
