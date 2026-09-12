from unittest.mock import patch

import pytest
from ingestion.gh_archive import BronzeEvent
from ingestion.ingest_to_bronze import ingest_window
from datetime import datetime, timezone

from ingestion.pipeline_state import get_last_successful_window


events = [
    BronzeEvent(
        source_event_id="1",
        event_type="PushEvent",
        event_created_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        source_window="2023-01-01-0",
        ingested_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        raw_event={"id": "1"},
    ),
    BronzeEvent(
        source_event_id="2",
        event_type="CreateEvent",
        event_created_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        source_window="2023-01-01-0",
        ingested_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        raw_event={"id": "2"},
    ),
    BronzeEvent(
        source_event_id="3",
        event_type="CreateEvent",
        event_created_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        source_window="2023-01-01-0",
        ingested_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        raw_event={"id": "3"},
    ),
]


@patch("ingestion.ingest_to_bronze.load_events", return_value=events)
def test_ingest_window(mock_load_events, connection):
    ingest_window(connection, "2023-01-01-0")
    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bronze.github_events
            """
        )

        count = cursor.fetchone()[0]
    assert count == len(events)

@patch("ingestion.ingest_to_bronze.load_events", return_value=events)
def test_transaction_failure(mock_load_events, connection):
    with pytest.raises(RuntimeError):
        ingest_window(
            connection,
            "2023-01-01-0",
            fail_after=2,
        )
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bronze.github_events
            """
        )
        count = cursor.fetchone()[0]

    last_window = get_last_successful_window(
        connection,
        "gh_archive_bronze",
        )
    
    assert count == 0
    assert last_window is None


@patch("ingestion.ingest_to_bronze.load_events", return_value=events)
def test_transaction_success_with_state(mock_load_events, connection):
    ingest_window(connection, "2023-01-01-0")
    last_window = get_last_successful_window(
    connection,
    "gh_archive_bronze",
    )

    assert last_window == "2023-01-01-0"