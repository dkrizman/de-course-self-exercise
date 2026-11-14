import os

import psycopg

from ingestion.ingest_to_bronze import ingest_window


def main() -> None:
    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as connection:
        ingest_window(connection)


if __name__ == "__main__":
    main()
