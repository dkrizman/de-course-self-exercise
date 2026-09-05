import pytest
import gzip
import io
import json
from unittest.mock import patch, Mock
from datetime import datetime

from ingestion.gh_archive import load_events, parse_events, build_url, download_gh_events, prepare_bronze_event

@pytest.fixture
def events():
    return [
    {'id': '26163418658',
 'type': 'PushEvent',
 'created_at': '2023-01-01T00:00:00Z'
},
 {'id': '26163418711',
 'type': 'CreateEvent',
 'actor': {'id': 101432083},
 'public': True,
 'created_at': '2023-01-01T00:00:00Z'}
]

def create_events_gz(events):
    buf = io.BytesIO()

    with gzip.GzipFile(fileobj=buf, mode="w") as f:
        for event in events:
            line = json.dumps(event) + "\n"
            f.write(line.encode("utf-8"))

    buf.seek(0)

    return buf

def test_parse_events(events):

    gz = create_events_gz(events)

    results = list(parse_events(gz))
    
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]['id'] == '26163418658'
    assert results[1]['id'] == '26163418711'


def test_build_url():
    window = '2023-01-01-0'
    final_url = build_url(window)
    assert final_url == 'https://data.gharchive.org/2023-01-01-0.json.gz'



def test_download_gh_events(events):
    gz_bytes = create_events_gz(events).read()

    with patch("ingestion.gh_archive.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.raw = io.BytesIO(gz_bytes)
        result = download_gh_events(build_url("2023-01-01-0"))

    mock_get.assert_called_once_with("https://data.gharchive.org/2023-01-01-0.json.gz", stream=True)
    mock_get.return_value.raise_for_status.assert_called_once()
    assert mock_get.return_value.raw.decode_content is False
    assert result.read() == gz_bytes

def test_load_events_full_chain(events):
    gz_bytes = create_events_gz(events).read()

    with patch("ingestion.gh_archive.requests.get") as mock_get:
        mock_response = Mock(status_code=200)
        mock_response.raw = io.BytesIO(gz_bytes)
        mock_get.return_value = mock_response

        results = list(load_events("2023-01-01-0"))

    assert len(results) == 2
    assert results[0].source_event_id == "26163418658"
    assert results[1].source_event_id == "26163418711"



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