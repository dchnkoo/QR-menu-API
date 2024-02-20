from ...API.ResponseModels.Register import RegisterResponseFail
from ...API.ResponseModels.Restaurant import RestaurantResponseSucces
from ...API.ResponseModels.Ingredients import Ingredient, IngredientGetResponse
from ...API.ResponseModels.Category import CategoryTable
from ...API.ResponseModels.Dishes import Dish

from ..Restaurant.func import (get_restaurant, register_restaurant,
                               delete_resturant)
from ..User.func import registration, delete_user
from ..User import users
from ..Category.func import add_category, delete_category

from .func import add_ingredient, get_ingredient, delete_ingredient
from ..Dishes.func import get_dishes, add_dish, delete_dish

import httpx
import pytest, pytest_asyncio


@pytest_asyncio.fixture(scope="module", params=users)
async def setup_user(client: httpx.AsyncClient, request):
    data = request.param

    status, user, token = await registration(client, data)

    assert status == 200 and RegisterResponseFail(**user)

    yield token

    status = await delete_user(client, token)
    assert status == 200

@pytest_asyncio.fixture(scope="module")
async def setup_retaurant(client: httpx.AsyncClient, setup_user: str):
    status, data = await register_restaurant(client, get_restaurant(),
                        setup_user)
    
    assert status == 200 and RestaurantResponseSucces(**data)

    yield setup_user

    status, _ = await delete_resturant(client, setup_user)
    assert status == 200

@pytest_asyncio.fixture(scope="module")
async def setup_categories(client: httpx.AsyncClient, setup_retaurant: str):
    categories = ({"category": "Десерти"},
                {"category": "Гарячі страви"},
                {"category": "Холодні страви"},
                {"category": "Напої"})
    
    temp = []
    for i in categories:
        status, data = await add_category(client, setup_retaurant, i)

        assert status == 200 and CategoryTable(**data)
        temp.append(data)

    yield setup_retaurant, temp

    status, value = await delete_category(client, setup_retaurant, {"type": "all"})

    assert status == 200 and ("msg" in value) is True


@pytest_asyncio.fixture(scope="module")
async def setup_dishes(client: httpx.AsyncClient, setup_categories: tuple[str, list[dict]]):
    token, data = setup_categories

    temp = []
    for i in data:
        category_id = i.get("id")
        for j in get_dishes(category_id):
            status, response = await add_dish(client, token, j)

            assert status == 200 and Dish(**response)
            temp.append(response)

    yield token, temp

    for i in data:
        category_id = i.get("id")

        for j in range(1, (len(data) * len(get_dishes(category_id))) + 1):
            status, response = await delete_dish(client, token, **{"category_id": category_id, "dish_id": j})

            assert status == 200 and ("msg" in response) is True


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def add_ingredient_fixture(client: httpx.AsyncClient, setup_dishes: tuple[str, list[dict]]):
    token, data = setup_dishes
    
    ingredients = []
    for i in data:
        dish_id = i.get("id")

        for j in get_ingredient(dish_id):
            status, response = await add_ingredient(client, token, j)

            assert status == 200 and Ingredient(**response)
            ingredients.append(response)

    yield token, ingredients

    for dish, ingredient in [(i["dish_id"], i["id"]) for i in ingredients]:
        status, response = await delete_ingredient(client, token, dish, ingredient)

        assert status == 200 and ("msg" in response) is True


@pytest.mark.asyncio
async def test_add_ingredient_fail(client: httpx.AsyncClient):
    request = await client.post("/api/admin/add/ingredient")

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_delete_ingredients_fail(client: httpx.AsyncClient):
    request = await client.delete("/api/admin/delete/ingredients")

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_ingredients_fail(client: httpx.AsyncClient):
    request = await client.get("/api/admin/get/ingredients")

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_ingredients(client: httpx.AsyncClient, add_ingredient_fixture: tuple[str, list[dict]]):
    get_corntone = [i async for i in add_ingredient_fixture]
    token, data = get_corntone[0][0], get_corntone[0][1]

    cookie = {"token": token}

    for i in [i["dish_id"] for i in data]:
        request = await client.get(f"/api/admin/get/ingredients?dish_id={i}", cookies=cookie)

        assert request.status_code == 200 and IngredientGetResponse(**request.json())


