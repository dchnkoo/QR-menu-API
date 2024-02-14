from ...API.ResponseModels.Restaurant import RestaurantResponseSucces
from ...API.ResponseModels.Register import RegisterResponseFail
from ...API.ResponseModels.Tables import GetTablesResponse

from ..Restaurant.func import delete_resturant, register_restaurant, get_restaurant
from ..User.func import registration, delete_user
from ..User import users

import pytest, pytest_asyncio
import httpx


@pytest_asyncio.fixture(scope="module", params=users)
async def setup(client: httpx.AsyncClient, request):
    data = request.param

    status, user, token = await registration(client, data)

    assert status == 200 and RegisterResponseFail(**user)

    status, data =  await register_restaurant(client, get_restaurant(image=True),
                        token)
    
    assert status == 200 and RestaurantResponseSucces(**data)

    yield token

    status, _ = await delete_resturant(client, token)
    assert status == 200

    status = await delete_user(client, token)
    assert status == 200

@pytest.mark.asyncio
async def test_create_tables_fail(client: httpx.AsyncClient):
    request = await client.post("/api/admin/create/tables")

    assert request.status_code == 403 and ("detail" in request.json()) is True


@pytest.mark.asyncio
async def test_delete_table_fail(client: httpx.AsyncClient):
    request = await client.delete(f"/api/admin/delete/tables")

    assert request.status_code == 403 and ("detail" in request.json()) is True

@pytest.mark.asyncio
async def test_get_tables_fail(client: httpx.AsyncClient):
    request = await client.get("/api/admin/get/tables")

    assert request.status_code == 403 and ("detail" in request.json()) is True


@pytest.mark.asyncio
async def test_create_tables_rgb_fail_le(client: httpx.AsyncClient, setup: str):
    cookie = {"token": setup}

    request = await client.post("/api/admin/create/tables", cookies=cookie,
                          json={"table_number": 100, "background": (-1, 255, 255)})
    
    assert request.status_code == 422


@pytest.mark.asyncio
async def test_create_tables_rgb_fail_ge(client: httpx.AsyncClient, setup: str):
    cookie = {"token": setup}

    request = await client.post("/api/admin/create/tables", cookies=cookie,
                          json={"table_number": 100, "background": (255, 255, 256)})
    
    assert request.status_code == 422


@pytest.mark.asyncio
async def test_create_tables_rgb_fail(client: httpx.AsyncClient, setup: str):
    cookie = {"token": setup}

    request = await client.post("/api/admin/create/tables", cookies=cookie,
                          json={"table_number": 100, "background": [255, 255, 255, 255]})
    
    assert request.status_code == 422



@pytest.mark.asyncio
async def test_create_tables(client: httpx.AsyncClient, setup: str):
    cookie = {"token": setup}

    request = await client.post("/api/admin/create/tables", cookies=cookie,
                          json={"table_number": 100})
    
    assert request.status_code == 200 and ("msg" in request.json()) is True

@pytest.mark.asyncio
async def test_create_tables_logo(client: httpx.AsyncClient, setup: str):
    cookie = {"token": setup}

    request = await client.post("/api/admin/create/tables", cookies=cookie,
                          json={"table_number": 1, "logo": True})
    
    assert request.status_code == 200
    
@pytest.mark.asyncio
@pytest.mark.parametrize("table", list(range(1, 11)))
async def test_delete_table(client: httpx.AsyncClient, setup: str, table: int):
    cookie = {"token": setup}

    request = await client.delete(f"/api/admin/delete/tables?type=table&table_number={table}", cookies=cookie)

    assert request.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("num", list(range(1, 9)))
async def test_get_tables(client: httpx.AsyncClient, num: int, setup: str):
    cookie = {"token": setup}

    request = await client.get(f"/api/admin/get/tables?page={num}", cookies=cookie)

    assert request.status_code == 200 and GetTablesResponse(**request.json())

@pytest.mark.asyncio
async def test_delete_table_all(client: httpx.AsyncClient, setup: str):
    cookie = {"token": setup}

    request = await client.delete(f"/api/admin/delete/tables?type=all", cookies=cookie)

    assert request.status_code == 200