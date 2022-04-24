"""Songs, albums, playlists tables

Revision ID: 7e820043c0d2
Revises: 
Create Date: 2022-04-24 12:27:54.579007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e820043c0d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_albums_id'), 'albums', ['id'], unique=False)
    op.create_index(op.f('ix_albums_title'), 'albums', ['title'], unique=False)
    op.create_table('playlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_playlists_id'), 'playlists', ['id'], unique=False)
    op.create_index(op.f('ix_playlists_title'), 'playlists', ['title'], unique=False)
    op.create_table('songs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_songs_id'), 'songs', ['id'], unique=False)
    op.create_index(op.f('ix_songs_title'), 'songs', ['title'], unique=False)
    op.create_table('playlists_songs',
    sa.Column('song_id', sa.Integer(), nullable=True),
    sa.Column('playlist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlists.id'], ),
    sa.ForeignKeyConstraint(['song_id'], ['songs.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlists_songs')
    op.drop_index(op.f('ix_songs_title'), table_name='songs')
    op.drop_index(op.f('ix_songs_id'), table_name='songs')
    op.drop_table('songs')
    op.drop_index(op.f('ix_playlists_title'), table_name='playlists')
    op.drop_index(op.f('ix_playlists_id'), table_name='playlists')
    op.drop_table('playlists')
    op.drop_index(op.f('ix_albums_title'), table_name='albums')
    op.drop_index(op.f('ix_albums_id'), table_name='albums')
    op.drop_table('albums')
    # ### end Alembic commands ###