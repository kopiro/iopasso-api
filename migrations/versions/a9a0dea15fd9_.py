"""empty message

Revision ID: a9a0dea15fd9
Revises: c4b88bb84225
Create Date: 2021-02-12 18:03:09.741007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9a0dea15fd9'
down_revision = 'c4b88bb84225'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('datetime', sa.DateTime(), nullable=True))
    op.drop_column('events', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('date', sa.DATE(), nullable=True))
    op.drop_column('events', 'datetime')
    # ### end Alembic commands ###
