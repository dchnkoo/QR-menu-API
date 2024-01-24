"""create tables

Revision ID: 18736e18a34a
Revises: 
Create Date: 2024-01-24 22:33:25.206718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18736e18a34a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authefication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hashf', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('hashf')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hashf', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('start_day', sa.VARCHAR(length=30), nullable=True),
    sa.Column('end_day', sa.VARCHAR(length=30), nullable=True),
    sa.Column('start_time', sa.VARCHAR(length=30), nullable=True),
    sa.Column('end_time', sa.VARCHAR(length=30), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['hashf'], ['authefication.hashf'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hashf')
    )
    op.create_table('categoryies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.VARCHAR(), nullable=False),
    sa.Column('url', sa.VARCHAR(), nullable=True),
    sa.Column('color', sa.VARCHAR(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ingredient', sa.VARCHAR(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('menu_link', sa.VARCHAR(), nullable=True),
    sa.Column('qr', sa.String(), nullable=True),
    sa.Column('table', sa.Integer(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.BLOB(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('url', sa.VARCHAR(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('comment', sa.VARCHAR(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categoryies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dishIngredient',
    sa.Column('dish_id', sa.Integer(), nullable=False),
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dish_id'], ['dishes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('dish_id', 'ingredient_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishIngredient')
    op.drop_table('dishes')
    op.drop_table('tables')
    op.drop_table('ingredients')
    op.drop_table('categoryies')
    op.drop_table('restaurant')
    op.drop_table('authefication')
    # ### end Alembic commands ###
