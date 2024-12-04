"""Supplies types data

Revision ID: 26f6c3c4fc3a
Revises: 73ba1f09e47f
Create Date: 2024-12-04 12:13:37.520193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26f6c3c4fc3a'
down_revision = '73ba1f09e47f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO "Supplies_types" (name) VALUES
        ('EPP'),
        ('Material de escritorio'),
        ('Material fungible'),
        ('Material de Vidrio'),
        ('Primers'),
        ('Reactivo');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM "Supplies_types" WHERE name IN ('EPP', 'Material de escritorio', 'Material fungible', 'Material de Vidrio', 'Primers', 'Reactivo');
        """
    )
