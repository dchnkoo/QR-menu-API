from ...API.ResponseModels.Register import RegisterResponseSucces
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

    status, user = await registration(client, data)

    assert status == 200 and RegisterResponseSucces(**user)

    yield user

    status = await delete_user(client, user.get("token"))

    assert status == 200


@pytest.mark.asyncio
async def test_register_restaurant_fail(client: httpx.AsyncClient, event_loop, setup_user: dict):
    status, _ = await register_restaurant(client, None, None, cookies=False)
    
    assert status == 403

@pytest.mark.asyncio
async def test_register_restaurant_fail_cookie(client: httpx.AsyncClient, event_loop, setup_user: dict):
    status, data = await register_restaurant(client, None, setup_user.get("token")[:20])

    assert status == 403 and ("detail" in data) is True

@pytest.mark.asyncio
async def test_register_restaurant(client: httpx.AsyncClient, event_loop, setup_user: dict):
    status, data = await register_restaurant(client, get_restaurant(), setup_user.get("token"))

    assert status == 200 and RestaurantResponseSucces(**data)

@pytest.mark.asyncio
async def test_restaurant_update_fail(client: httpx.AsyncClient, event_loop, setup_user: dict):
    request = await client.patch('/api/admin/update/restaurant')

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_update_fail_cookie(client: httpx.AsyncClient, event_loop, setup_user: dict):
    cookie = {"token": setup_user.get("token")[:20]}

    request = await client.patch('/api/admin/update/restaurant', cookies=cookie)

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_update(client: httpx.AsyncClient, event_loop, setup_user: dict):
    cookie = {"token": setup_user.get("token")}
    
    request = await client.patch('/api/admin/update/restaurant',
                          cookies=cookie, json=get_restaurant_update())

    update = request.json()
    assert request.status_code == 200 and RestaurantResponseSucces(**update)

@pytest.mark.asyncio
async def test_restaurant_get_fail(client: httpx.AsyncClient, event_loop, setup_user: dict):
    request = await client.get('/api/admin/get/restaurant')

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_get_fail_cookie(client: httpx.AsyncClient, event_loop, setup_user: dict):
    cookie = {"token": setup_user.get("token")[:20]}

    request = await client.get('/api/admin/get/restaurant', cookies=cookie)

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_restaurant_get(client: httpx.AsyncClient, event_loop, setup_user: dict):
    cookie = {"token": setup_user.get("token")}

    request = await client.get('/api/admin/get/restaurant', cookies=cookie)

    assert request.status_code == 200 and RestaurantResponseSucces(**request.json())

@pytest.mark.asyncio
async def test_restaurant_delete_fail(client: httpx.AsyncClient, event_loop, setup_user: dict):
    status, data = await delete_resturant(client, None, cookies=False)

    assert status == 403 and ("detail" in data) is True

@pytest.mark.asyncio
async def test_restaurant_delete_fail_cookie(client: httpx.AsyncClient, event_loop, setup_user: dict):
    status, data = await delete_resturant(client, setup_user.get("token")[:20])

    assert status == 403 and ("detail" in data) is True

@pytest.mark.asyncio
async def test_restaurant_delete(client: httpx.AsyncClient, event_loop, setup_user: dict):
    status, data = await delete_resturant(client, setup_user.get("token"))

    assert status == 200 and ("msg" in data) is True