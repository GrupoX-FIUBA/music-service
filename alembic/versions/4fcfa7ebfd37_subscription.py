"""Subscription

Revision ID: 4fcfa7ebfd37
Revises: 18505f7611f1
Create Date: 2022-05-10 16:32:52.325994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fcfa7ebfd37'
down_revision = '18505f7611f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('subscription', sa.Integer(), nullable=False, server_default = sa.text("0")))
    op.add_column('songs', sa.Column('subscription', sa.Integer(), nullable=False, server_default = sa.text("0")))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('songs', 'subscription')
    op.drop_column('albums', 'subscription')
    # ### end Alembic commands ###
