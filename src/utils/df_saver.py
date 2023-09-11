import io
import os
import psycopg2
from typing import Literal
from polars import DataFrame
from datetime import datetime
from dotenv import load_dotenv
from dataclasses import dataclass
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential

load_dotenv()
# TODO: Refactor for dependency injection


@dataclass
class azure_storage:
    mode: Literal["csv", "parquet"] = "parquet"

    def save_df(self, df: DataFrame, table_name: str) -> None:
        azure_storage_url: str = os.environ["AZURE_STORAGE_BLOB_URL"]
        azure_credential = DefaultAzureCredential()
        container_name: str = "best-city"

        b_buf = io.BytesIO()

        if self.mode == "parquet":
            df.write_parquet(b_buf)
        if self.mode == "csv":
            df.write_csv(b_buf)
        b_buf.seek(0)

        container_client = ContainerClient(
            account_url=azure_storage_url, container_name=container_name, credential=azure_credential
        )
        container_client.upload_blob(
            f"{table_name}/{table_name}_{datetime.now().date()}.{self.mode}", b_buf, overwrite=True
        )


@dataclass
class postgres_db:
    def save_df(self, df: DataFrame, table_name: str) -> None:
        conn_uri: str = os.environ["POSTGRES_CONN_URI"]
        csv_file = io.BytesIO()
        df.write_csv(csv_file)
        csv_file.seek(0)

        conn = psycopg2.connect(conn_uri)
        cursor = conn.cursor()
        query = f"COPY raw.{table_name} FROM stdin WITH CSV HEADER ON CONFLICT (submission_id) DO NOTHING"
        cursor.copy_expert(sql=query, file=csv_file)

        conn.commit()

        cursor.close()
        conn.close()
