"""drop_table_ticket

Revision ID: bc72b805fff7
Revises: 4c64287c3dbf
Create Date: 2025-06-05 17:46:22.072216

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bc72b805fff7"
down_revision: Union[str, None] = "4c64287c3dbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("tickets")


def downgrade() -> None:
    """Downgrade schema."""
    pass
