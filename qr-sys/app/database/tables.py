from .db.Meta.data import metadata
from sqlalchemy import (Table, Column, Integer, String,
                        ForeignKey, VARCHAR, ARRAY)


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
    Column('address', String, nullable=True),
    Column('start_day', VARCHAR(30), nullable=True),
    Column('end_day', VARCHAR(30), nullable=True),
    Column('start_time', VARCHAR(30), nullable=True),
    Column('end_time', VARCHAR(30), nullable=True), 
    Column('logo', String, nullable=True) 
)

categories = Table(
    'categories',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('category', VARCHAR, nullable=False),
    Column('color', ARRAY(Integer)),
    Column('restaurant_id', Integer, ForeignKey('restaurant.id', ondelete='CASCADE'))
)

dishes = Table(
    'dishes',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('img', String),
    Column('name', VARCHAR, nullable=False),
    Column('price', Integer),
    Column('weight', Integer),
    Column('comment', VARCHAR),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE')),
    Column('restaurant_id', Integer, ForeignKey("restaurant.id", ondelete="CASCADE"))
)

ingredients = Table(
    'ingredients',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('ingredient', VARCHAR),
    Column("dish_id", Integer, ForeignKey('dishes.id', ondelete="CASCADE")),
    Column('restaurant_id', Integer, ForeignKey('restaurant.id', ondelete='CASCADE')),
)

tables = Table(
    'tables',
    metadata,

    Column('id', Integer, primary_key=True),
    Column('menu_link', VARCHAR),
    Column('qr', String),
    Column('table_number', Integer),
    Column('restaurant_id', Integer,
           ForeignKey('restaurant.id', ondelete='CASCADE'))
)