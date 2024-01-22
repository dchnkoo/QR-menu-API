from app.framework import app, db, t
from ..database.tables import (authefication, restaurant,
                               categories, dishes, ingredients,
                               dishIngredient, tables)


# API
@app.get('/api/login/{key}')
async def login(key: str):
    return {'user': key}