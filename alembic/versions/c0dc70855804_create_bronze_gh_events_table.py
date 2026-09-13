"""create bronze gh events table

Revision ID: c0dc70855804
Revises: 
Create Date: 2026-09-04 18:51:32.697326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0dc70855804'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE SCHEMA bronze;

    CREATE TABLE bronze.github_events (
        source_event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        event_created_at TIMESTAMPTZ NOT NULL,
        source_window TEXT NOT NULL,
        ingested_at TIMESTAMPTZ NOT NULL,
        raw_event JSONB NOT NULL
    );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP TABLE IF EXISTS bronze.github_events;
    DROP SCHEMA IF EXISTS bronze;
    """)
