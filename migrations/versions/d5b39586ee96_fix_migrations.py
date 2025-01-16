"""fix migrations

Revision ID: d5b39586ee96
Revises: 
Create Date: 2025-01-16 12:19:50.575423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5b39586ee96'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_category_id'), 'category', ['id'], unique=False, schema='public')
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_genre_id'), 'genre', ['id'], unique=False, schema='public')
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_role_id'), 'role', ['id'], unique=False, schema='public')
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('eng_title', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('avatar', sa.VARCHAR(), nullable=False),
    sa.Column('release_year', sa.Date(), nullable=False),
    sa.Column('director', sa.VARCHAR(), nullable=False),
    sa.Column('country', sa.VARCHAR(), nullable=False),
    sa.Column('part', sa.Integer(), nullable=False),
    sa.Column('age_restriction', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('producer', sa.VARCHAR(), nullable=False),
    sa.Column('screenwriter', sa.VARCHAR(), nullable=False),
    sa.Column('operator', sa.VARCHAR(), nullable=False),
    sa.Column('composer', sa.VARCHAR(), nullable=False),
    sa.Column('artist', sa.VARCHAR(), nullable=False),
    sa.Column('editor', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['public.category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_movie_id'), 'movie', ['id'], unique=False, schema='public')
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avatar', sa.VARCHAR(length=255), nullable=True),
    sa.Column('username', sa.VARCHAR(length=255), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=20), nullable=False),
    sa.Column('hashed_password', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('country', sa.VARCHAR(length=255), nullable=True),
    sa.Column('gender', sa.CHAR(length=1), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['public.role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_user_email'), 'user', ['email'], unique=True, schema='public')
    op.create_index(op.f('ix_public_user_id'), 'user', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_user_phone'), 'user', ['phone'], unique=True, schema='public')
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('heart', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_favorite_id'), 'favorite', ['id'], unique=False, schema='public')
    op.create_table('genre_movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['public.genre.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_genre_movie_id'), 'genre_movie', ['id'], unique=False, schema='public')
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('like', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_like_id'), 'like', ['id'], unique=False, schema='public')
    op.create_table('movie_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_movie_comments_id'), 'movie_comments', ['id'], unique=False, schema='public')
    op.create_table('movie_rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_movie_rating_id'), 'movie_rating', ['id'], unique=False, schema='public')
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('photo', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_photo_id'), 'photo', ['id'], unique=False, schema='public')
    op.create_table('poster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('photo', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_poster_id'), 'poster', ['id'], unique=False, schema='public')
    op.create_table('social_networks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_social_networks_id'), 'social_networks', ['id'], unique=False, schema='public')
    op.create_table('trailer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('url_trailer', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['public.movie.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_trailer_id'), 'trailer', ['id'], unique=False, schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_public_trailer_id'), table_name='trailer', schema='public')
    op.drop_table('trailer', schema='public')
    op.drop_index(op.f('ix_public_social_networks_id'), table_name='social_networks', schema='public')
    op.drop_table('social_networks', schema='public')
    op.drop_index(op.f('ix_public_poster_id'), table_name='poster', schema='public')
    op.drop_table('poster', schema='public')
    op.drop_index(op.f('ix_public_photo_id'), table_name='photo', schema='public')
    op.drop_table('photo', schema='public')
    op.drop_index(op.f('ix_public_movie_rating_id'), table_name='movie_rating', schema='public')
    op.drop_table('movie_rating', schema='public')
    op.drop_index(op.f('ix_public_movie_comments_id'), table_name='movie_comments', schema='public')
    op.drop_table('movie_comments', schema='public')
    op.drop_index(op.f('ix_public_like_id'), table_name='like', schema='public')
    op.drop_table('like', schema='public')
    op.drop_index(op.f('ix_public_genre_movie_id'), table_name='genre_movie', schema='public')
    op.drop_table('genre_movie', schema='public')
    op.drop_index(op.f('ix_public_favorite_id'), table_name='favorite', schema='public')
    op.drop_table('favorite', schema='public')
    op.drop_index(op.f('ix_public_user_phone'), table_name='user', schema='public')
    op.drop_index(op.f('ix_public_user_id'), table_name='user', schema='public')
    op.drop_index(op.f('ix_public_user_email'), table_name='user', schema='public')
    op.drop_table('user', schema='public')
    op.drop_index(op.f('ix_public_movie_id'), table_name='movie', schema='public')
    op.drop_table('movie', schema='public')
    op.drop_index(op.f('ix_public_role_id'), table_name='role', schema='public')
    op.drop_table('role', schema='public')
    op.drop_index(op.f('ix_public_genre_id'), table_name='genre', schema='public')
    op.drop_table('genre', schema='public')
    op.drop_index(op.f('ix_public_category_id'), table_name='category', schema='public')
    op.drop_table('category', schema='public')
    # ### end Alembic commands ###
