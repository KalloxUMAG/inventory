"""Equipment Types

Revision ID: 9ea766df193f
Revises: e3a3f51701d0
Create Date: 2024-06-24 15:24:25.703129

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9ea766df193f"
down_revision = "e3a3f51701d0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Equipment_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("Equipments", sa.Column("equipment_type_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None, "Equipments", "Equipment_types", ["equipment_type_id"], ["id"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "Equipments", type_="foreignkey")
    op.drop_column("Equipments", "equipment_type_id")
    op.drop_table("Equipment_types")
    # ### end Alembic commands ###
