"""create phone Number column in users table

Revision ID: f0806085b22e
Revises: 
Create Date: 2026-02-15 16:12:16.949760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0806085b22e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable = True))



def downgrade() -> None:
    """Downgrade schema."""
    pass
