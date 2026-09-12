

from datetime import datetime, timezone

import pytest
from unittest.mock import patch

from ingestion.gh_archive import BronzeEvent
from ingestion.ingest_to_bronze import ingest_window
from ingestion.pipeline_state import get_last_successful_window, set_last_successful_window


def test_get_last_successful_window_when_not_exist(connection):
    # Implement the test for get_last_successful_window function
    last_window = get_last_successful_window(connection, "test_pipeline")
    assert last_window is None

def test_get_last_successful_window_when_exist(connection):
    # Implement the test for get_last_successful_window function when the window exists
    from datetime import datetime, timezone
    window = "2023-01-01-00"
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO pipeline.pipeline_state
                (pipeline_name, last_successful_window, updated_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (pipeline_name) DO UPDATE
                SET last_successful_window = EXCLUDED.last_successful_window,
                    updated_at = EXCLUDED.updated_at;
            """,
            (
                "test_pipeline",
                window,
                datetime.now(timezone.utc),
            ),
        )
        connection.commit()

    last_window = get_last_successful_window(connection, "test_pipeline")
    assert last_window == window

def test_set_last_successful_window_creates_state(connection):
    set_last_successful_window(
        connection,
        "test_pipeline",
        "2023-01-01-00",
    )

    last_window = get_last_successful_window(
        connection,
        "test_pipeline",
    )

    assert last_window == "2023-01-01-00"

def test_set_last_successful_window_updates_existing_state(connection):
    set_last_successful_window(
        connection,
        "test_pipeline",
        "2023-01-01-00",
    )

    set_last_successful_window(
        connection,
        "test_pipeline",
        "2023-01-01-01",
    )

    last_window = get_last_successful_window(
        connection,
        "test_pipeline",
    )

    assert last_window == "2023-01-01-01"

def fake_events():
    now = datetime.now(timezone.utc)
    for i in range(5):
        yield BronzeEvent(
            source_event_id=str(i),
            event_type="PushEvent",
            event_created_at=now,
            source_window="2023-01-01-01",
            ingested_at=now,
            raw_event={"id": str(i), "type": "PushEvent"},
        )

def test_successful_window(connection):

    set_last_successful_window(
                connection,
                "test_pipeline",
                "2023-01-01-00"
            )
    connection.commit()
    with patch("ingestion.ingest_to_bronze.load_events", return_value=fake_events()):
        with pytest.raises(RuntimeError):
            ingest_window(
                connection,
                "2023-01-01-01",
                fail_after=2,
            )

    last_window = get_last_successful_window(connection, "test_pipeline")
    assert last_window == "2023-01-01-00"
