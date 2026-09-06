from unittest.mock import patch
from ingestion.gh_archive import BronzeEvent
from ingestion.ingest_to_bronze import ingest_window
from datetime import datetime, timezone


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
        source_event_id="2",
        event_type="CreateEvent",
        event_created_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        source_window="2023-01-01-0",
        ingested_at=datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        raw_event={"id": "2"},
    ),
]


@patch("ingestion.ingest_to_bronze.load_events", return_value=events)
def test_ingest_window(mock_load_events, connection):

    mock_load_events.return_value = events
    try:
        ingest_window(connection, "2023-01-01-0")
    except Exception as e:
        print(f"Error occurred: {e}")
        pass
    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bronze.github_events
            """
        )

        count = cursor.fetchone()[0]
    assert count == len(events) - 1 # One duplicate event should be ignored
