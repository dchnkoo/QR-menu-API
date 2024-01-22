from . import metadata
from sqlalchemy import (Table, Column, Integer, String,
                        ForeignKey, VARCHAR, DateTime, BLOB)


# create tables here 
authefication = Table(
    'authefication',
    metadata,
    
    Column('id', Integer, primary_key=True),
    Column('hashf', String, unique=True, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False)
)

restaurant = Table(
    'restaurant',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('hashf', String, ForeignKey('authefication.hashf', ondelete='CASCADE'), 
                   unique=True, nullable=False),
    Column('name', String, nullable=False),
    Column('address', String, nullable=False),
    Column('start_day', VARCHAR, nullable=True),
    Column('end_day', VARCHAR, nullable=True),
    Column('start_time', DateTime, nullable=True),
    Column('end_time', DateTime, nullable=True) 
)

categories = Table(
    'categoryies',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('category', VARCHAR, nullable=False),
    Column('url', VARCHAR),
    Column('color', VARCHAR),
    Column('restaurant_id', Integer, ForeignKey('restaurant.id', ondelete='CASCADE'))
)

dishes = Table(
    'dishes',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('img', BLOB),
    Column('name', VARCHAR, nullable=False),
    Column('url', VARCHAR),
    Column('price', Integer),
    Column('weight', Integer),
    Column('comment', VARCHAR),
    Column('category_id', Integer, ForeignKey('categoryies.id', ondelete='CASCADE'))
)

ingredients = Table(
    'ingredients',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('ingredient', VARCHAR),
    Column('restaurant_id', Integer, ForeignKey('restaurant.id', ondelete='CASCADE')),
)

dishIngredient = Table(
    'dishIngredient',
    metadata,

    Column('dish_id', Integer, 
           ForeignKey('dishes.id', ondelete='CASCADE'), 
           primary_key=True),

    Column('ingredient_id', Integer,
           ForeignKey('ingredients.id', ondelete='CASCADE'),
           primary_key=True)
)

tables = Table(
    'tables',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('menu_link', VARCHAR),
    Column('qr', BLOB),
    Column('restaurant_id', Integer,
           ForeignKey('restaurant.id', ondelete='CASCADE'))
)