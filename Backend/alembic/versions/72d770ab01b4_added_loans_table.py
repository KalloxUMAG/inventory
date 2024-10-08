"""Added Loans Table

Revision ID: 72d770ab01b4
Revises: e14b1a0f4fe4
Create Date: 2024-09-05 13:45:26.699788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72d770ab01b4'
down_revision = 'e14b1a0f4fe4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Loans',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['Lots.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Loans')
    # ### end Alembic commands ###
