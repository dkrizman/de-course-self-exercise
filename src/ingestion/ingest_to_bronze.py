from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from ingestion.pipeline_state import get_last_successful_window, set_last_successful_window
from typing import Any

from psycopg.types.json import Json

from ingestion.gh_archive import load_events

PIPELINE_NAME = "gh_archive_bronze"
INITIAL_WINDOW = "2023-01-01-0"

def ingest_window(connection, fail_after=None):
    prev_window = get_last_successful_window(connection, PIPELINE_NAME)
    if prev_window is None:
        window = INITIAL_WINDOW
    else:
        window = next_window(prev_window)
    try:
        with connection.cursor() as cursor:
            for index, event in enumerate(load_events(window)):
                if fail_after is not None and index == fail_after:
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


def next_window(last_successful_window):
    date_part, hour_part = last_successful_window.rsplit("-", 1)

    dt = datetime.strptime(date_part, "%Y-%m-%d").replace(
        hour=int(hour_part)
    )

    dt += timedelta(hours=1)

    return f"{dt.strftime('%Y-%m-%d')}-{dt.hour}"