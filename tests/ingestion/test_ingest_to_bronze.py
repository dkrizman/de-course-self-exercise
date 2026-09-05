from ingestion.ingest_to_bronze import prepare_bronze_event
from datetime import datetime


def test_prepare_bronze_event() -> None:
    event = {
        "id": "1",
        "type": "PushEvent",
        "created_at": "2023-01-01T00:00:00Z",
    }

    window = "2023-01-01-00"

    ingested_at = "2026-09-04T10:00:00Z"

    bronze_event = prepare_bronze_event(event=event, source_window=window, ingested_at=ingested_at)
    assert bronze_event.source_event_id == event["id"]
    assert bronze_event.event_type == event["type"]
    assert bronze_event.event_created_at == datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
    assert bronze_event.source_window == window
    assert bronze_event.ingested_at == datetime.fromisoformat(ingested_at.replace("Z", "+00:00"))
    assert bronze_event.raw_event == event