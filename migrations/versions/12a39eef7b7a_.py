"""empty message

Revision ID: 12a39eef7b7a
Revises: 67fc2ff11df8
Create Date: 2020-05-03 23:14:17.825592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12a39eef7b7a'
down_revision = '67fc2ff11df8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###