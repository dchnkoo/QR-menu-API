from ...API.ResponseModels.Register import RegisterResponseFail
from ...API.ResponseModels.Restaurant import RestaurantResponseSucces

from .func import (get_restaurant, get_restaurant_update, 
                   delete_resturant, register_restaurant)
from ..User.func import registration, delete_user
from ..User import users


import pytest, pytest_asyncio
import httpx


@pytest_asyncio.fixture(scope="module", params=users)
async def setup_user(client: httpx.AsyncClient, request):
    data = request.param

    status, user, token = await registration(client, data)

    assert status == 200 and RegisterResponseFail(**user)

    yield token

    status = await delete_user(client, token)

    assert status == 200

@pytest.mark.asyncio
async def test_register_restaurant_fail_cookie(client: httpx.AsyncClient):
    status, data = await register_restaurant(client, None, None)

    assert status == 401 and ("detail" in data) is True


@pytest.mark.asyncio
async def test_restaurant_update_fail(client: httpx.AsyncClient):
    request = await client.patch('/api/admin/update/restaurant')

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_get_fail(client: httpx.AsyncClient):
    request = await client.get('/api/admin/get/restaurant')

    assert request.status_code == 401 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_delete_fail(client: httpx.AsyncClient):
    status, data = await delete_resturant(client, None, cookies=False)

    assert status == 401 and ("detail" in data) is True

@pytest.mark.asyncio
async def test_register_restaurant(client: httpx.AsyncClient, setup_user: str):
    status, data = await register_restaurant(client, get_restaurant(), setup_user)

    assert status == 200 and RestaurantResponseSucces(**data)


@pytest.mark.asyncio
async def test_restaurant_update(client: httpx.AsyncClient, setup_user: str):
    cookie = {"token": setup_user}
    
    request = await client.patch('/api/admin/update/restaurant',
                          cookies=cookie, json=get_restaurant_update())

    update = request.json()
    assert request.status_code == 200 and RestaurantResponseSucces(**update)

@pytest.mark.asyncio
async def test_restaurant_get(client: httpx.AsyncClient, setup_user: str):
    cookie = {"token": setup_user}

    request = await client.get('/api/admin/get/restaurant', cookies=cookie)

    assert request.status_code == 200 and RestaurantResponseSucces(**request.json())

@pytest.mark.asyncio
async def test_restaurant_delete(client: httpx.AsyncClient, setup_user: str):
    status, data = await delete_resturant(client, setup_user)

    assert status == 200 and ("msg" in data) is True