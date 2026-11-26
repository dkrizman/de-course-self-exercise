{{
    config(
        materialized='view'
    )
}}

SELECT
    DATE(event_created_at) AS activity_date,
    repo_name,
    COUNT(*) AS event_count,
    COUNT(DISTINCT actor_id) AS unique_actors

FROM {{ ref('silver_github_events') }}

GROUP BY
    DATE(event_created_at),
    repo_name