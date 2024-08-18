"""add fcm_token to user

Revision ID: 60fd756f433b
Revises: 748b77734caa
Create Date: 2024-08-11 14:38:16.125254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60fd756f433b'
down_revision: Union[str, None] = '748b77734caa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
