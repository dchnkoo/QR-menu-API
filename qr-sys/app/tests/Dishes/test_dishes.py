from ...API.ResponseModels.Register import RegisterResponseFail
from ...API.ResponseModels.Restaurant import RestaurantResponseSucces
from ...API.ResponseModels.Category import CategoryTable
from ...API.ResponseModels.Dishes import Dish, DishResponseList

from ..Restaurant.func import (get_restaurant, register_restaurant,
                               delete_resturant)
from ..User.func import registration, delete_user
from ..User import users
from ..Category.func import add_category, delete_category

from .func import get_dishes, add_dish, delete_dish

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

@pytest.mark.asyncio
async def test_add_dish_fail(client: httpx.AsyncClient):
    request = await client.post('/api/admin/add/dish')

    assert request.status_code == 401 and ("detail" in request.json()) is True


@pytest.mark.asyncio
async def test_get_dish_fail(client: httpx.AsyncClient):
    request = await client.get('/api/admin/get/dish')

    assert request.status_code == 401 and ("detail" in request.json()) is True


@pytest.mark.asyncio
async def test_delete_dish_fail(client: httpx.AsyncClient):
    request = await client.delete('/api/admin/delete/dish')

    assert request.status_code == 401 and ("detail" in request.json()) is True


@pytest.mark.asyncio
async def test_add_dish(client: httpx.AsyncClient, setup_categories: tuple[str, list[dict]]):
    token, data = setup_categories

    for i in data:
        category_id = i.get("id")
        for j in get_dishes(category_id):
            status, response = await add_dish(client, token, j)

            assert status == 200 and Dish(**response)

@pytest.mark.asyncio
async def test_get_dish(client: httpx.AsyncClient, setup_categories: tuple[str, list[dict]]):
    token, data = setup_categories

    cookie = {"token": token}

    for i in data:
        request = await client.get(f"/api/admin/get/dish?category_id={i.get('id')}",
                             cookies=cookie)
        
        assert request.status_code == 200 and DishResponseList(**request.json())

@pytest.mark.asyncio
async def test_delete_dishes(client: httpx.AsyncClient, setup_categories: tuple[str, list[dict]]):
    token, data = setup_categories

    for i in data:
        category_id = i.get("id")

        for j in range(1, (len(data) * len(get_dishes(category_id))) + 1):
            status, response = await delete_dish(client, token, **{"category_id": category_id, "dish_id": j})

            assert status == 200 and ("msg" in response) is True

