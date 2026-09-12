"""add pipeline state

Revision ID: d067210906e6
Revises: c0dc70855804
Create Date: 2026-09-07 23:12:41.939064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd067210906e6'
down_revision: Union[str, Sequence[str], None] = 'c0dc70855804'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE SCHEMA pipeline;

        CREATE TABLE pipeline.pipeline_state (
            pipeline_name TEXT PRIMARY KEY,
            last_successful_window TEXT NOT NULL,
            updated_at TIMESTAMP NOT NULL
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP TABLE IF EXISTS pipeline.pipeline_state;
        DROP SCHEMA IF EXISTS pipeline;
        """
    )
