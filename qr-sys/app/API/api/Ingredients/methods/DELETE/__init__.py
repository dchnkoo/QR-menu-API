from .....ResponseModels.Register import RegisterResponseFail
from ......framework import app, jwt, db, logger
from ......database.tables import ingredients
from .....tags import INGREDIENTS

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends


@app.delete("/api/admin/delete/ingredients", tags=[INGREDIENTS], dependencies=[Depends(jwt)])
async def delete_ingredients(ingredient_id: int, dish_id: int) -> RegisterResponseFail:
    try: await db.async_delete_data(ingredients, and__=(ingredients.c.id == ingredient_id,
                                                        ingredients.c.dish_id == dish_id))
    except Exception as e:
        logger.error(f"Помилка під час видалення ingredient_id: {ingredient_id}\n\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки запиту")
    
    return JSONResponse(status_code=200, content={"msg": f"Інгредіент id: {ingredient_id} успішно видаленний"})    