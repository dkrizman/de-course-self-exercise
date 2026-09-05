from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class BronzeEvent:
    source_event_id: str
    event_type: str
    event_created_at: datetime
    source_window: str
    ingested_at: datetime
    raw_event: dict[str, Any]

def prepare_bronze_event(event: dict[str, Any], source_window: str, ingested_at: str) -> BronzeEvent:
    return BronzeEvent(
        source_event_id=event["id"],
        event_type=event["type"],
        event_created_at=datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")),
        source_window=source_window,
        ingested_at=datetime.fromisoformat(ingested_at.replace("Z", "+00:00")),
        raw_event=event,
    )