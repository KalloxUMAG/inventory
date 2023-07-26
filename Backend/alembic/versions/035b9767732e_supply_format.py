"""supply format

Revision ID: 035b9767732e
Revises: ac5e13275a1f
Create Date: 2023-07-25 14:59:59.330450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '035b9767732e'
down_revision = 'ac5e13275a1f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Example',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Example')
    # ### end Alembic commands ###