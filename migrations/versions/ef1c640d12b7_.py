"""empty message

Revision ID: ef1c640d12b7
Revises: 3ddf0a24fdb3
Create Date: 2024-06-22 14:18:51.162766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef1c640d12b7'
down_revision: Union[str, None] = '3ddf0a24fdb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
