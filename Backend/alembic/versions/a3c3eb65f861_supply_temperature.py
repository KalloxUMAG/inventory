"""Supply temperature

Revision ID: a3c3eb65f861
Revises: 26f6c3c4fc3a
Create Date: 2024-12-05 12:49:37.453069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3c3eb65f861'
down_revision = '26f6c3c4fc3a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Supplies', sa.Column('temperature', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Supplies', 'temperature')
    # ### end Alembic commands ###
