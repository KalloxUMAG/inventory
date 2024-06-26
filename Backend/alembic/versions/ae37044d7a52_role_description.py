"""role description

Revision ID: ae37044d7a52
Revises: a9b0a1fa96b9
Create Date: 2023-12-13 15:55:16.525121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae37044d7a52'
down_revision = 'a9b0a1fa96b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Roles', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Roles', 'description')
    # ### end Alembic commands ###
