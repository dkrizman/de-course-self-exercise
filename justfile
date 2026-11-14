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
