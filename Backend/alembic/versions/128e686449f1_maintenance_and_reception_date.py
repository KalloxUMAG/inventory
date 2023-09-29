"""maintenance and reception date

Revision ID: 128e686449f1
Revises: b34c4ac29ab9
Create Date: 2023-09-26 14:10:50.829561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '128e686449f1'
down_revision = 'b34c4ac29ab9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Equipments', sa.Column('next_maintenance', sa.Date(), nullable=True))
    op.add_column('Lots', sa.Column('reception_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Lots', 'reception_date')
    op.drop_column('Equipments', 'next_maintenance')
    # ### end Alembic commands ###
