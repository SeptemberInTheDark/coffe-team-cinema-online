"""увше movie table

Revision ID: 712607ce604e
Revises: 2fbda032f9cb
Create Date: 2024-10-10 12:13:27.916662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '712607ce604e'
down_revision: Union[str, None] = '2fbda032f9cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'url_movie',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_constraint('ratings_user_id_fkey', 'ratings', type_='foreignkey')
    op.create_foreign_key(None, 'ratings', 'users', ['user_id'], ['id'], referent_schema='public')
    op.drop_constraint('reviews_user_id_fkey', 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'users', ['user_id'], ['id'], referent_schema='public')
    op.drop_constraint('users_role_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', schema='public', type_='foreignkey')
    op.create_foreign_key('users_role_id_fkey', 'users', 'roles', ['role_id'], ['id'])
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key('reviews_user_id_fkey', 'reviews', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.create_foreign_key('ratings_user_id_fkey', 'ratings', 'users', ['user_id'], ['id'])
    op.alter_column('movies', 'url_movie',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###