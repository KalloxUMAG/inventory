"""Role permissions

Revision ID: 246c8bca542b
Revises: 921c415a0374
Create Date: 2024-07-29 14:16:03.514272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '246c8bca542b'
down_revision = '921c415a0374'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Roles', sa.Column('create', sa.Boolean(), nullable=False))
    op.add_column('Roles', sa.Column('read', sa.Boolean(), nullable=False))
    op.add_column('Roles', sa.Column('update', sa.Boolean(), nullable=False))
    op.add_column('Roles', sa.Column('delete', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Roles', 'delete')
    op.drop_column('Roles', 'update')
    op.drop_column('Roles', 'read')
    op.drop_column('Roles', 'create')
    # ### end Alembic commands ###