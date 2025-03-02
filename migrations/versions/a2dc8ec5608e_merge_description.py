"""merge description

Revision ID: a2dc8ec5608e
Revises: 02a6b5d6b4fb, b9a2b3c5d457
Create Date: 2025-02-25 08:49:15.395139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2dc8ec5608e'
down_revision: Union[str, None] = ('02a6b5d6b4fb', 'b9a2b3c5d457')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
