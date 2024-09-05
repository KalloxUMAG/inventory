"""Removed Loans table

Revision ID: e14b1a0f4fe4
Revises: 78e2fd9aca91
Create Date: 2024-09-05 13:44:15.724474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e14b1a0f4fe4'
down_revision = '78e2fd9aca91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Loans')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Loans',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lot_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('start_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['Lots.id'], name='Loans_lot_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='Loans_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='loans_pk')
    )
    # ### end Alembic commands ###
