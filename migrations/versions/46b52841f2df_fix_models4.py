"""fix models4

Revision ID: 46b52841f2df
Revises: 713b26bbded2
Create Date: 2025-01-22 09:21:00.744067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46b52841f2df'
down_revision: Union[str, None] = '713b26bbded2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('actor_movie_actor_id_fkey', 'actor_movie', type_='foreignkey')
    op.drop_constraint('actor_movie_movie_id_fkey', 'actor_movie', type_='foreignkey')
    op.create_foreign_key(None, 'actor_movie', 'actor', ['actor_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'actor_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('favorite_movie_id_fkey', 'favorite', type_='foreignkey')
    op.drop_constraint('favorite_user_id_fkey', 'favorite', type_='foreignkey')
    op.create_foreign_key(None, 'favorite', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'favorite', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('genre_movie_movie_id_fkey', 'genre_movie', type_='foreignkey')
    op.drop_constraint('genre_movie_genre_id_fkey', 'genre_movie', type_='foreignkey')
    op.create_foreign_key(None, 'genre_movie', 'genre', ['genre_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'genre_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('like_movie_id_fkey', 'like', type_='foreignkey')
    op.drop_constraint('like_user_id_fkey', 'like', type_='foreignkey')
    op.create_foreign_key(None, 'like', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'like', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column(
        'movie',
        'operator',
        type_=sa.JSON(),
        existing_type=sa.String(),  # Укажите текущий тип столбца
        postgresql_using="operator::json"
    )
    op.drop_constraint('movie_category_id_fkey', 'movie', type_='foreignkey')
    op.create_foreign_key(None, 'movie', 'category', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('movie_comments_user_id_fkey', 'movie_comments', type_='foreignkey')
    op.drop_constraint('movie_comments_movie_id_fkey', 'movie_comments', type_='foreignkey')
    op.create_foreign_key(None, 'movie_comments', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'movie_comments', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('movie_rating_user_id_fkey', 'movie_rating', type_='foreignkey')
    op.drop_constraint('movie_rating_movie_id_fkey', 'movie_rating', type_='foreignkey')
    op.create_foreign_key(None, 'movie_rating', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'movie_rating', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('news_actor_actor_id_fkey', 'news_actor', type_='foreignkey')
    op.drop_constraint('news_actor_news_id_fkey', 'news_actor', type_='foreignkey')
    op.create_foreign_key(None, 'news_actor', 'user', ['actor_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'news_actor', 'news', ['news_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('news_comments_news_id_fkey', 'news_comments', type_='foreignkey')
    op.drop_constraint('news_comments_user_id_fkey', 'news_comments', type_='foreignkey')
    op.create_foreign_key(None, 'news_comments', 'news', ['news_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'news_comments', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('news_views_user_id_fkey', 'news_views', type_='foreignkey')
    op.drop_constraint('news_views_news_id_fkey', 'news_views', type_='foreignkey')
    op.create_foreign_key(None, 'news_views', 'news', ['news_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'news_views', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('photo_movie_id_fkey', 'photo', type_='foreignkey')
    op.create_foreign_key(None, 'photo', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('poster_movie_id_fkey', 'poster', type_='foreignkey')
    op.create_foreign_key(None, 'poster', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('reward_actor_actor_id_fkey', 'reward_actor', type_='foreignkey')
    op.drop_constraint('reward_actor_reward_id_fkey', 'reward_actor', type_='foreignkey')
    op.create_foreign_key(None, 'reward_actor', 'reward', ['reward_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'reward_actor', 'actor', ['actor_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('reward_movie_movie_id_fkey', 'reward_movie', type_='foreignkey')
    op.drop_constraint('reward_movie_reward_id_fkey', 'reward_movie', type_='foreignkey')
    op.create_foreign_key(None, 'reward_movie', 'reward', ['reward_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'reward_movie', 'movie', ['movie_id'], ['id'], source_schema='public', referent_schema='public')
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
    op.drop_constraint(None, 'reward_movie', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'reward_movie', schema='public', type_='foreignkey')
    op.create_foreign_key('reward_movie_reward_id_fkey', 'reward_movie', 'reward', ['reward_id'], ['id'])
    op.create_foreign_key('reward_movie_movie_id_fkey', 'reward_movie', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'reward_actor', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'reward_actor', schema='public', type_='foreignkey')
    op.create_foreign_key('reward_actor_reward_id_fkey', 'reward_actor', 'reward', ['reward_id'], ['id'])
    op.create_foreign_key('reward_actor_actor_id_fkey', 'reward_actor', 'actor', ['actor_id'], ['id'])
    op.drop_constraint(None, 'poster', schema='public', type_='foreignkey')
    op.create_foreign_key('poster_movie_id_fkey', 'poster', 'movie', ['movie_id'], ['id'])
    op.drop_constraint(None, 'photo', schema='public', type_='foreignkey')
    op.create_foreign_key('photo_movie_id_fkey', 'photo', 'movie', ['movie_id'], ['id'])
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
    op.create_foreign_key('news_actor_news_id_fkey', 'news_actor', 'news', ['news_id'], ['id'])
    op.create_foreign_key('news_actor_actor_id_fkey', 'news_actor', 'user', ['actor_id'], ['id'])
    op.drop_constraint(None, 'movie_rating', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'movie_rating', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_rating_movie_id_fkey', 'movie_rating', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('movie_rating_user_id_fkey', 'movie_rating', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'movie_comments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'movie_comments', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_comments_movie_id_fkey', 'movie_comments', 'movie', ['movie_id'], ['id'])
    op.create_foreign_key('movie_comments_user_id_fkey', 'movie_comments', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'movie', schema='public', type_='foreignkey')
    op.create_foreign_key('movie_category_id_fkey', 'movie', 'category', ['category_id'], ['id'])
    op.alter_column('movie', 'operator',
               existing_type=sa.JSON(),
               type_=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'like', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'like', schema='public', type_='foreignkey')
    op.create_foreign_key('like_user_id_fkey', 'like', 'user', ['user_id'], ['id'])
    op.create_foreign_key('like_movie_id_fkey', 'like', 'movie', ['movie_id'], ['id'])
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
    # ### end Alembic commands ###
