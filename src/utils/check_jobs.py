import os
import psycopg2
import polars as pl


def data_jobs_in_db() -> bool:
    """Checks if there is jobs data in db
    -- returns True if jobs data is present in the db"""
    conn_uri: str = os.environ["POSTGRES_CONN_URI"]
    conn = psycopg2.connect(conn_uri)
    query = """SELECT * FROM staging.jobs"""
    df = pl.read_database(query, conn)
    conn.close()

    return not df.is_empty()


if __name__ == "__main__":
    data_jobs_in_db()
