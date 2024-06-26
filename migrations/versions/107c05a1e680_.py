"""empty message

Revision ID: 107c05a1e680
Revises: ef1c640d12b7
Create Date: 2024-06-22 14:27:37.214188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '107c05a1e680'
down_revision: Union[str, None] = 'ef1c640d12b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_confirmacao',
    sa.Column('con_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('con_medicacaoId', sa.Integer(), nullable=False),
    sa.Column('con_horarioId', sa.Integer(), nullable=False),
    sa.Column('con_dataHorario', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('con_id')
    )
    op.create_table('tbl_horario',
    sa.Column('hor_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hor_horario', sa.Time(), nullable=False),
    sa.Column('hor_medicacao', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('hor_id')
    )
    op.create_table('tbl_medicacao',
    sa.Column('med_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('med_nome', sa.String(), nullable=False),
    sa.Column('med_descricao', sa.String(), nullable=False),
    sa.Column('med_tipo', sa.String(), nullable=False),
    sa.Column('med_quantidade', sa.Integer(), nullable=False),
    sa.Column('med_dataInicio', sa.Date(), nullable=False),
    sa.Column('med_dataFinal', sa.Date(), nullable=False),
    sa.Column('med_perfilId', sa.Integer(), nullable=False),
    sa.Column('med_estado', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('med_id')
    )
    op.create_table('tbl_monitoramento',
    sa.Column('mon_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mon_sintomasId', sa.Integer(), nullable=False),
    sa.Column('mon_perfilId', sa.Integer(), nullable=False),
    sa.Column('mon_dataHorario', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('mon_id')
    )
    op.create_table('tbl_sintomas',
    sa.Column('sin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sin_nome', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('sin_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_sintomas')
    op.drop_table('tbl_monitoramento')
    op.drop_table('tbl_medicacao')
    op.drop_table('tbl_horario')
    op.drop_table('tbl_confirmacao')
    # ### end Alembic commands ###
