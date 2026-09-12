from dataclasses import dataclass
from datetime import datetime, timezone
from ingestion.pipeline_state import set_last_successful_window
from typing import Any

from psycopg.types.json import Json

from ingestion.gh_archive import load_events

PIPELINE_NAME = "gh_archive_bronze"

def ingest_window(connection, window, fail_after=None):
    try:
        with connection.cursor() as cursor:
            for index, event in enumerate(load_events(window)):
                if fail_after is not None and index == fail_after:
                    connection.rollback()
                    raise RuntimeError("Failing after processing the specified number of events")
                cursor.execute(
                """
                INSERT INTO bronze.github_events
                    (source_event_id, event_type, event_created_at, source_window, ingested_at, raw_event)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_event_id) DO NOTHING;
                """,
                (
                    event.source_event_id,
                    event.event_type,
                    event.event_created_at,
                    event.source_window,
                    event.ingested_at,
                    Json(event.raw_event),
                ),
            )
        set_last_successful_window(connection,PIPELINE_NAME, window)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e