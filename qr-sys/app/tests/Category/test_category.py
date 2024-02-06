from ...API.ResponseModels.Register import RegisterResponseSucces
from ...API.ResponseModels.Restaurant import RestaurantResponseSucces
from ...API.ResponseModels.Category import CategoryTable

from ..Restaurant.func import (get_restaurant, register_restaurant,
                               delete_resturant)
from ..User.func import registration, delete_user
from ..User import users
from .func import add_category, delete_category

import pytest, pytest_asyncio
import httpx


@pytest_asyncio.fixture(scope="module", params=users)
async def setup(client: httpx.AsyncClient, request):
    data = request.param

    status, user = await registration(client, data)

    assert status == 200 and RegisterResponseSucces(**user)
    token = user.get("token")

    status, data = await register_restaurant(client, get_restaurant(),
                        token)
    assert status == 200 and RestaurantResponseSucces(**data)

    yield token

    status, _ = await delete_resturant(client, token)
    assert status == 200

    status = await delete_user(client, token)
    assert status == 200


@pytest.mark.asyncio
async def test_add_category_fail(client: httpx.AsyncClient, event_loop):
    status, data = await add_category(client, None, cookies=False)

    assert status == 403 and ("detail" in data) is True


@pytest.mark.asyncio
async def test_add_category_fail_cookie(client: httpx.AsyncClient, setup: str, event_loop):
    status, data = await add_category(client, setup[:20])

    assert status == 403 and ("detail" in data) is True

@pytest.mark.asyncio
@pytest.fixture(scope="function", params=[({"category": "Десерти", "color": "red"},
                                        {"category": "Гарячі страви", "color": "blue"},
                                        {"category": "Холодні страви", "color": "purple"},
                                        {"category": "Напої", "color": "black"})])
async def add_category_fixture(client: httpx.AsyncClient, setup: str, request, event_loop):
    data = request.param

    categories = []
    for i in data: 
        status, category = await add_category(client, setup, i)

        assert status == 200 and CategoryTable(**category)
        categories.append(category)

    yield categories


@pytest.mark.asyncio
async def test_get_categories_fail(client: httpx.AsyncClient, event_loop):
    request = await client.get('/api/admin/get/categories')

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_categories_fail_cookie(client: httpx.AsyncClient, setup: str, event_loop):
    cookie = {"token": setup[:20]}

    request = await client.get('/api/admin/get/categories', cookies=cookie)

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_categories(client: httpx.AsyncClient, setup: str, event_loop):
    cookie = {"token": setup}

    request = await client.get("/api/admin/get/categories", cookies=cookie)

    assert request.status_code == 200

@pytest.mark.asyncio
async def test_get_full_categories_fail(client: httpx.AsyncClient, event_loop):
    request = await client.get('/api/admin/get-full-info/categories')

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_full_categories_fail_cookie(client: httpx.AsyncClient, setup: str, event_loop):
    cookie = {"token": setup[:20]}

    request = await client.get('/api/admin/get-full-info/categories', cookies=cookie)

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_full_categories(client: httpx.AsyncClient, setup: str, add_category_fixture, event_loop):
    cookie = {"token": setup}

    request = await client.get('/api/admin/get-full-info/categories', cookies=cookie)

    assert request.status_code == 200

@pytest.mark.asyncio
async def test_delete_categories_fail(client: httpx.AsyncClient, event_loop):
    request = await client.delete('/api/admin/delete/categories')

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_delete_categories_fail_cookie(client: httpx.AsyncClient, setup: str, event_loop):
    cookie = {"token": setup[:20]}

    request = await client.delete('/api/admin/delete/categories', cookies=cookie)

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_delete_category(client: httpx.AsyncClient, setup: str, add_category_fixture: tuple[dict], event_loop):
    data = [i[0] async for i in add_category_fixture]

    for i in data:
        status, data = await delete_category(client, setup, {"type": "category", "category_id": i.get("id")})

        assert status == 200 and ("msg" in data) is True

@pytest.mark.asyncio
async def test_delete_category_all(client: httpx.AsyncClient, setup: str, add_category_fixture: tuple[dict], event_loop):
    status, data = await delete_category(client, setup, {"type": "all", "category_id": 0}, )

    assert status == 200 and ("msg" in data) is True