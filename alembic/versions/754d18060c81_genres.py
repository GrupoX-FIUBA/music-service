"""Genres

Revision ID: 754d18060c81
Revises: 81838ad6f94a
Create Date: 2022-05-09 16:49:38.148519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '754d18060c81'
down_revision = '81838ad6f94a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genres_id'), 'genres', ['id'], unique=False)
    op.create_index(op.f('ix_genres_title'), 'genres', ['title'], unique=False)
    op.add_column('albums', sa.Column('genre_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'albums', 'genres', ['genre_id'], ['id'])
    op.add_column('playlists', sa.Column('colaborativa', sa.Boolean(), nullable=True))
    op.add_column('songs', sa.Column('genre_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'songs', 'genres', ['genre_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'songs', type_='foreignkey')
    op.drop_column('songs', 'genre_id')
    op.drop_column('playlists', 'colaborativa')
    op.drop_constraint(None, 'albums', type_='foreignkey')
    op.drop_column('albums', 'genre_id')
    op.drop_index(op.f('ix_genres_title'), table_name='genres')
    op.drop_index(op.f('ix_genres_id'), table_name='genres')
    op.drop_table('genres')
    # ### end Alembic commands ###
