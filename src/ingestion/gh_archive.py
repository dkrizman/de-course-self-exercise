
from datetime import datetime, timezone
import io
import gzip
import json

import requests

from ingestion.ingest_to_bronze import prepare_bronze_event

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

def load_events(window) -> iter:
    url = build_url(window)
    raw = download_gh_events(url)
    ingested_at = datetime.now(timezone.utc).isoformat()
    for event in parse_events(raw):
        yield prepare_bronze_event(event, window, ingested_at)