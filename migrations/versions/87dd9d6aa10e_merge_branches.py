"""merge branches

Revision ID: 87dd9d6aa10e
Revises: 026566fed50c, 4ed36426576d
Create Date: 2026-04-16 14:49:19.769947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87dd9d6aa10e'
down_revision: Union[str, Sequence[str], None] = ('026566fed50c', '4ed36426576d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
