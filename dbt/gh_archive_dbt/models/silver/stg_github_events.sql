SELECT
    source_event_id,
    event_type,
    event_created_at,
    source_window,
    ingested_at,
    raw_event
FROM {{ source('bronze', 'github_events') }}