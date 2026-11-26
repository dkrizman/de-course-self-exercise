SELECT *
FROM {{ ref('gold_daily_repo_activity') }}
WHERE event_count <= 0
   OR unique_actors > event_count