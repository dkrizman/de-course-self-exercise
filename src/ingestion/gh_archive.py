
from dataclasses import dataclass
from datetime import datetime, timezone
import io
import gzip
import json

from typing import Any, Iterator
import requests

def parse_events(gz):
    with gzip.GzipFile(fileobj=gz, mode='r') as f:
        for line in f:
            yield json.loads(line)

def build_url(window):
    return f'https://data.gharchive.org/{window}.json.gz'

def download_gh_events(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    response.raw.decode_content = False  # keep gzip bytes raw, don't let urllib3 auto-decompress
    return response.raw

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

def load_events(window) -> Iterator[BronzeEvent]:
    url = build_url(window)
    raw = download_gh_events(url)
    ingested_at = datetime.now(timezone.utc).isoformat()
    for event in parse_events(raw):
        yield prepare_bronze_event(event, window, ingested_at)