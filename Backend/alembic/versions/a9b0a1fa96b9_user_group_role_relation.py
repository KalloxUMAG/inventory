"""user group role relation

Revision ID: a9b0a1fa96b9
Revises: 128e686449f1
Create Date: 2023-12-13 11:39:17.030151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9b0a1fa96b9'
down_revision = '128e686449f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User_Group_Role_Relation',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['Groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['Roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'group_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User_Group_Role_Relation')
    op.drop_table('Roles')
    # ### end Alembic commands ###
