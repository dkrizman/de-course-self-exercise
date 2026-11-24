# Start PostgreSQL and app
up:
    docker compose up -d --build db
    docker compose build app

# Apply pending database migrations
migrate:
    docker compose run --rm app alembic upgrade head

# Stop services
down:
    docker compose down

# Run Bronze ingestion
ingest:
    docker compose run --rm app python -m main

# Show PostgreSQL logs
db-logs:
    docker compose logs -f db

# Open PostgreSQL CLI from the app container
psql:
    docker compose exec db psql -U pipeline -d pipeline -P pager=off

DBT_PROJECT := "/app/dbt/gh_archive_dbt"
DBT_PROFILES := "/app/.dbt"

dbt-init:
    docker compose run --rm app sh -c 'cd /app/dbt && dbt init gh_archive_dbt'

dbt-debug:
    docker compose run --rm app dbt debug --project-dir {{DBT_PROJECT}} --profiles-dir {{DBT_PROFILES}}

dbt-parse:
    docker compose run --rm app dbt parse --project-dir {{DBT_PROJECT}} --profiles-dir {{DBT_PROFILES}}

dbt-run:
    docker compose run --rm app dbt run --project-dir {{DBT_PROJECT}} --profiles-dir {{DBT_PROFILES}}

dbt-test:
    docker compose run --rm app dbt test --project-dir {{DBT_PROJECT}} --profiles-dir {{DBT_PROFILES}}
