"""add fcm_token to user

Revision ID: 748b77734caa
Revises: 1676c191196a
Create Date: 2024-08-11 14:37:10.797888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '748b77734caa'
down_revision: Union[str, None] = '1676c191196a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
