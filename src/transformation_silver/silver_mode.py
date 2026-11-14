from dataclasses import dataclass
from datetime import datetime
from ingestion.gh_archive import BronzeEvent


@dataclass
class SilverEvent:
    source_event_id: str
    event_type: str
    event_created_at: datetime
    source_window: str
    ingested_at: datetime
    actor_login: str


def transform_to_silver(bronze_event: BronzeEvent) -> SilverEvent:

    return SilverEvent(
        source_event_id=bronze_event.source_event_id,
        event_type=bronze_event.event_type,
        event_created_at=bronze_event.event_created_at,
        source_window=bronze_event.source_window,
        ingested_at=bronze_event.ingested_at,
        actor_login=bronze_event.raw_event["actor"]["login"],
    )