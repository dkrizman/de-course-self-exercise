from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from psycopg.types.json import Json

from ingestion.gh_archive import load_events



def ingest_window(connection, window):
    with connection.cursor() as cursor:
        for event in load_events(window):
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
    connection.commit()