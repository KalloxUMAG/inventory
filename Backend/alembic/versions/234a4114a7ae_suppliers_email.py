"""Suppliers email

Revision ID: 234a4114a7ae
Revises: a3c3eb65f861
Create Date: 2024-12-10 14:44:19.889222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '234a4114a7ae'
down_revision = 'a3c3eb65f861'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Suppliers', sa.Column('email', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Suppliers', 'email')
    # ### end Alembic commands ###