{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='source_event_id'
    )
}}

SELECT
    source_event_id,
    event_type,
    event_created_at,
    ingested_at,

    (raw_event -> 'actor' ->> 'id')::BIGINT AS actor_id,
    raw_event -> 'actor' ->> 'login' AS actor_login,

    (raw_event -> 'repo' ->> 'id')::BIGINT AS repo_id,
    raw_event -> 'repo' ->> 'name' AS repo_name

FROM {{ ref('stg_github_events') }} AS bronze

-- {% if is_incremental() %}

-- WHERE NOT EXISTS (
--     SELECT 1
--     FROM {{ this }} AS silver
--     WHERE silver.source_event_id = bronze.source_event_id
-- )

-- {% endif %}