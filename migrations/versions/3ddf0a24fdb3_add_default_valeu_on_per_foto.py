"""add default valeu on per_foto

Revision ID: 3ddf0a24fdb3
Revises: 7f58e9b04893
Create Date: 2024-05-25 13:40:26.598578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ddf0a24fdb3'
down_revision: Union[str, None] = '7f58e9b04893'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
