"""fix models

Revision ID: 02799b42fa0e
Revises: f5dac8a05b5d
Create Date: 2025-01-17 14:20:29.055968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02799b42fa0e'
down_revision: Union[str, None] = 'f5dac8a05b5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('actor', 'eng_full_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('actor', 'biography',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('actor', 'avatar',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('actor', 'height',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('actor', 'date_of_birth',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('actor', 'place_of_birth',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('actor_movie_actor_id_fkey', 'actor_movie', type_='foreignkey')
    op.drop_constraint('actor_movie_movie_id_fkey', 'actor_movie', type_='foreignkey')
    op.create_foreign_key(None, 'actor_movie', 'actor', ['actor_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'actor_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('favorite_movie_id_fkey', 'favorite', type_='foreignkey')
    op.drop_constraint('favorite_user_id_fkey', 'favorite', type_='foreignkey')
    op.create_foreign_key(None, 'favorite', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'favorite', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('genre_movie_movie_id_fkey', 'genre_movie', type_='foreignkey')
    op.drop_constraint('genre_movie_genre_id_fkey', 'genre_movie', type_='foreignkey')
    op.create_foreign_key(None, 'genre_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'genre_movie', 'genre', ['genre_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('like_user_id_fkey', 'like', type_='foreignkey')
    op.drop_constraint('like_movie_id_fkey', 'like', type_='foreignkey')
    op.create_foreign_key(None, 'like', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'like', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('movie', sa.Column('actors', sa.VARCHAR(), nullable=True))
    op.alter_column('movie', 'url',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('movie', 'eng_title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('movie', 'avatar',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'release_year',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('movie', 'director',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'country',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'part',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('movie', 'age_restriction',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('movie', 'duration',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('movie', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('movie', 'producer',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'screenwriter',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'operator',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'composer',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movie', 'editor',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('movie_category_id_fkey', 'movie', type_='foreignkey')
    op.create_foreign_key(None, 'movie', 'category', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_column('movie', 'artist')
    op.alter_column('movie_comments', 'text',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_constraint('movie_comments_user_id_fkey', 'movie_comments', type_='foreignkey')
    op.drop_constraint('movie_comments_movie_id_fkey', 'movie_comments', type_='foreignkey')
    op.create_foreign_key(None, 'movie_comments', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'movie_comments', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('movie_rating', 'rating',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('movie_rating_movie_id_fkey', 'movie_rating', type_='foreignkey')
    op.drop_constraint('movie_rating_user_id_fkey', 'movie_rating', type_='foreignkey')
    op.create_foreign_key(None, 'movie_rating', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'movie_rating', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('news', 'sub_title',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_constraint('news_actor_news_id_fkey', 'news_actor', type_='foreignkey')
    op.drop_constraint('news_actor_actor_id_fkey', 'news_actor', type_='foreignkey')
    op.create_foreign_key(None, 'news_actor', 'news', ['news_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'news_actor', 'user', ['actor_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('news_comments_news_id_fkey', 'news_comments', type_='foreignkey')
    op.drop_constraint('news_comments_user_id_fkey', 'news_comments', type_='foreignkey')
    op.create_foreign_key(None, 'news_comments', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'news_comments', 'news', ['news_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('news_views_user_id_fkey', 'news_views', type_='foreignkey')
    op.drop_constraint('news_views_news_id_fkey', 'news_views', type_='foreignkey')
    op.create_foreign_key(None, 'news_views', 'news', ['news_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'news_views', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('photo', 'photo',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('photo_movie_id_fkey', 'photo', type_='foreignkey')
    op.create_foreign_key(None, 'photo', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('poster', 'photo',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('poster_movie_id_fkey', 'poster', type_='foreignkey')
    op.create_foreign_key(None, 'poster', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('reward', 'avatar',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('reward', 'nomination',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('reward_actor', 'year',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('reward_actor_reward_id_fkey', 'reward_actor', type_='foreignkey')
    op.drop_constraint('reward_actor_actor_id_fkey', 'reward_actor', type_='foreignkey')
    op.create_foreign_key(None, 'reward_actor', 'actor', ['actor_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'reward_actor', 'reward', ['reward_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('reward_movie', 'year',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('reward_movie_reward_id_fkey', 'reward_movie', type_='foreignkey')
    op.drop_constraint('reward_movie_movie_id_fkey', 'reward_movie', type_='foreignkey')
    op.create_foreign_key(None, 'reward_movie', 'reward', ['reward_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'reward_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('social_networks_user_id_fkey', 'social_networks', type_='foreignkey')
    op.create_foreign_key(None, 'social_networks', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('trailer', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('trailer', 'url_trailer',
               existing_type=sa.TEXT(),
               nullable=True)
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
    op.alter_column('trailer', 'url_trailer',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('trailer', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'social_networks', schema='public', type_='foreignkey')
    op.create_foreign_key('social_networks_user_id_fkey', 'social_networks', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'reward_movie', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'reward_movie', schema='public', type_='foreignkey')
    op.create_foreign_key('reward_movie_movie_id_fkey', 'reward_movie', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('reward_movie_reward_id_fkey', 'reward_movie', 'reward', ['reward_id'], ['id'])
    op.alter_column('reward_movie', 'year',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'reward_actor', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'reward_actor', schema='public', type_='foreignkey')
    op.create_foreign_key('reward_actor_actor_id_fkey', 'reward_actor', 'actor', ['actor_id'], ['id'])
    op.create_foreign_key('reward_actor_reward_id_fkey', 'reward_actor', 'reward', ['reward_id'], ['id'])
    op.alter_column('reward_actor', 'year',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('reward', 'nomination',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('reward', 'avatar',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'poster', schema='public', type_='foreignkey')
    op.create_foreign_key('poster_movie_id_fkey', 'poster', 'movie', ['movie_id'], ['id'])
    op.alter_column('poster', 'photo',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'photo', schema='public', type_='foreignkey')
    op.create_foreign_key('photo_movie_id_fkey', 'photo', 'movie', ['movie_id'], ['id'])
    op.alter_column('photo', 'photo',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'news_views', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'news_views', schema='public', type_='foreignkey')
    op.create_foreign_key('news_views_news_id_fkey', 'news_views', 'news', ['news_id'], ['id'])
    op.create_foreign_key('news_views_user_id_fkey', 'news_views', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'news_comments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'news_comments', schema='public', type_='foreignkey')
    op.create_foreign_key('news_comments_user_id_fkey', 'news_comments', 'user', ['user_id'], ['id'])
    op.create_foreign_key('news_comments_news_id_fkey', 'news_comments', 'news', ['news_id'], ['id'])
    op.drop_constraint(None, 'news_actor', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'news_actor', schema='public', type_='foreignkey')
    op.create_foreign_key('news_actor_actor_id_fkey', 'news_actor', 'user', ['actor_id'], ['id'])
    op.create_foreign_key('news_actor_news_id_fkey', 'news_actor', 'news', ['news_id'], ['id'])
    op.alter_column('news', 'sub_title',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_constraint(None, 'movie_rating', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'movie_rating', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_rating_user_id_fkey', 'movie_rating', 'user', ['user_id'], ['id'])
    op.create_foreign_key('movie_rating_movie_id_fkey', 'movie_rating', 'movie', ['movie_id'], ['id'])
    op.alter_column('movie_rating', 'rating',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'movie_comments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'movie_comments', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_comments_movie_id_fkey', 'movie_comments', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('movie_comments_user_id_fkey', 'movie_comments', 'user', ['user_id'], ['id'])
    op.alter_column('movie_comments', 'text',
               existing_type=sa.TEXT(),
               nullable=False)
    op.add_column('movie', sa.Column('artist', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'movie', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_category_id_fkey', 'movie', 'category', ['category_id'], ['id'])
    op.alter_column('movie', 'editor',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'composer',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'operator',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'screenwriter',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'producer',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('movie', 'duration',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('movie', 'age_restriction',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('movie', 'part',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('movie', 'country',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'director',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'release_year',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('movie', 'avatar',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('movie', 'eng_title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('movie', 'url',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('movie', 'actors')
    op.drop_constraint(None, 'like', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'like', schema='public', type_='foreignkey')
    op.create_foreign_key('like_movie_id_fkey', 'like', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('like_user_id_fkey', 'like', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'genre_movie', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'genre_movie', schema='public', type_='foreignkey')
    op.create_foreign_key('genre_movie_genre_id_fkey', 'genre_movie', 'genre', ['genre_id'], ['id'])
    op.create_foreign_key('genre_movie_movie_id_fkey', 'genre_movie', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'favorite', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'favorite', schema='public', type_='foreignkey')
    op.create_foreign_key('favorite_user_id_fkey', 'favorite', 'user', ['user_id'], ['id'])
    op.create_foreign_key('favorite_movie_id_fkey', 'favorite', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'actor_movie', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'actor_movie', schema='public', type_='foreignkey')
    op.create_foreign_key('actor_movie_movie_id_fkey', 'actor_movie', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('actor_movie_actor_id_fkey', 'actor_movie', 'actor', ['actor_id'], ['id'])
    op.alter_column('actor', 'place_of_birth',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('actor', 'date_of_birth',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('actor', 'height',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('actor', 'avatar',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('actor', 'biography',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('actor', 'eng_full_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
