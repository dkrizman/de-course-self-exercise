import pytest
from ingestion.gh_archive import prepare_bronze_event
from datetime import datetime, timezone
from transformation_silver.silver_mode import SilverEvent
from transformation_silver.silver_mode import transform_to_silver

raw_event = {
    "id": "1",
    "type": "PushEvent",
    "created_at": "2023-01-01T00:00:00Z",
    "actor": {"login": "test_user"}
}

bronze_event = prepare_bronze_event(event=raw_event, source_window="2023-01-01-0", ingested_at="2026-09-04T10:00:00Z")

def test_transform_to_silver():

    silver_event = transform_to_silver(bronze_event)

    assert silver_event.source_event_id == "1"
    assert silver_event.event_type == "PushEvent"
    assert silver_event.event_created_at == datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert silver_event.source_window == "2023-01-01-0"
    assert silver_event.ingested_at == datetime(2026, 9, 4, 10, 0, tzinfo=timezone.utc)
    assert silver_event.actor_login == "test_user"