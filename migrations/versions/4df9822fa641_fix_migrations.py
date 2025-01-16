"""fix migrations

Revision ID: 4df9822fa641
Revises: 3865859e7415
Create Date: 2025-01-16 12:07:16.226265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4df9822fa641'
down_revision: Union[str, None] = '3865859e7415'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ratings_movie_id_fkey', 'ratings', type_='foreignkey')
    op.drop_constraint('reviews_movie_id_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('actor_movies_movie_id_fkey', 'actor_movies', type_='foreignkey')
    op.drop_constraint('reviews_user_id_fkey', 'reviews', type_='foreignkey')
    op.drop_table('movies')
    op.drop_table('actor_movies')
    op.drop_table('actors')
    op.drop_table('genres')
    op.drop_index('ix_public_roles_id', table_name='roles')
    op.drop_constraint('users_role_id_fkey', 'users', type_='foreignkey')
    op.drop_table('roles')
    op.drop_table('ratings')
    op.drop_index('ix_public_users_email', table_name='users')
    op.drop_index('ix_public_users_id', table_name='users')
    op.drop_index('ix_public_users_phone', table_name='users')
    op.drop_table('users')
    op.drop_table('reviews')
    op.drop_constraint('favorite_user_id_fkey', 'favorite', type_='foreignkey')
    op.drop_constraint('favorite_movie_id_fkey', 'favorite', type_='foreignkey')
    op.create_foreign_key(None, 'favorite', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'favorite', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('genre_movie_genre_id_fkey', 'genre_movie', type_='foreignkey')
    op.drop_constraint('genre_movie_movie_id_fkey', 'genre_movie', type_='foreignkey')
    op.create_foreign_key(None, 'genre_movie', 'genre', ['genre_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'genre_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('like_movie_id_fkey', 'like', type_='foreignkey')
    op.drop_constraint('like_user_id_fkey', 'like', type_='foreignkey')
    op.create_foreign_key(None, 'like', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'like', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('movie_category_id_fkey', 'movie', type_='foreignkey')
    op.create_foreign_key(None, 'movie', 'category', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('movie_comments_movie_id_fkey', 'movie_comments', type_='foreignkey')
    op.drop_constraint('movie_comments_user_id_fkey', 'movie_comments', type_='foreignkey')
    op.create_foreign_key(None, 'movie_comments', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'movie_comments', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('movie_rating_movie_id_fkey', 'movie_rating', type_='foreignkey')
    op.drop_constraint('movie_rating_user_id_fkey', 'movie_rating', type_='foreignkey')
    op.create_foreign_key(None, 'movie_rating', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'movie_rating', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('photo_movie_id_fkey', 'photo', type_='foreignkey')
    op.create_foreign_key(None, 'photo', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('poster_movie_id_fkey', 'poster', type_='foreignkey')
    op.create_foreign_key(None, 'poster', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('social_networks_user_id_fkey', 'social_networks', type_='foreignkey')
    op.create_foreign_key(None, 'social_networks', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('trailer_movie_id_fkey', 'trailer', type_='foreignkey')
    op.create_foreign_key(None, 'trailer', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('user_role_id_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', schema='public', type_='foreignkey')
    op.create_foreign_key('user_role_id_fkey', 'user', 'role', ['role_id'], ['id'])
    op.drop_constraint(None, 'trailer', schema='public', type_='foreignkey')
    op.create_foreign_key('trailer_movie_id_fkey', 'trailer', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'social_networks', schema='public', type_='foreignkey')
    op.create_foreign_key('social_networks_user_id_fkey', 'social_networks', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'poster', schema='public', type_='foreignkey')
    op.create_foreign_key('poster_movie_id_fkey', 'poster', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'photo', schema='public', type_='foreignkey')
    op.create_foreign_key('photo_movie_id_fkey', 'photo', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'movie_rating', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'movie_rating', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_rating_user_id_fkey', 'movie_rating', 'user', ['user_id'], ['id'])
    op.create_foreign_key('movie_rating_movie_id_fkey', 'movie_rating', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'movie_comments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'movie_comments', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_comments_user_id_fkey', 'movie_comments', 'user', ['user_id'], ['id'])
    op.create_foreign_key('movie_comments_movie_id_fkey', 'movie_comments', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'movie', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_category_id_fkey', 'movie', 'category', ['category_id'], ['id'])
    op.drop_constraint(None, 'like', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'like', schema='public', type_='foreignkey')
    op.create_foreign_key('like_user_id_fkey', 'like', 'user', ['user_id'], ['id'])
    op.create_foreign_key('like_movie_id_fkey', 'like', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'genre_movie', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'genre_movie', schema='public', type_='foreignkey')
    op.create_foreign_key('genre_movie_movie_id_fkey', 'genre_movie', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('genre_movie_genre_id_fkey', 'genre_movie', 'genre', ['genre_id'], ['id'])
    op.drop_constraint(None, 'favorite', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'favorite', schema='public', type_='foreignkey')
    op.create_foreign_key('favorite_movie_id_fkey', 'favorite', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('favorite_user_id_fkey', 'favorite', 'user', ['user_id'], ['id'])
    op.create_table('reviews',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review_text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='reviews_movie_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='reviews_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='reviews_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='users_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_public_users_phone', 'users', ['phone'], unique=True)
    op.create_index('ix_public_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_public_users_email', 'users', ['email'], unique=True)
    op.create_table('ratings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='ratings_movie_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='ratings_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='ratings_pkey')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey')
    )
    op.create_index('ix_public_roles_id', 'roles', ['id'], unique=False)
    op.create_table('genres',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('genres_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='genres_pkey'),
    sa.UniqueConstraint('name', name='genres_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('actors',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('actors_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='actors_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('actor_movies',
    sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], name='actor_movies_actor_id_fkey'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='actor_movies_movie_id_fkey'),
    sa.PrimaryKeyConstraint('actor_id', 'movie_id', name='actor_movies_pkey')
    )
    op.create_table('movies',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url_movie', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('photo', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('release_year', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('director', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['genre_name'], ['genres.name'], name='movies_genre_name_fkey'),
    sa.PrimaryKeyConstraint('id', name='movies_pkey')
    )
    # ### end Alembic commands ###
