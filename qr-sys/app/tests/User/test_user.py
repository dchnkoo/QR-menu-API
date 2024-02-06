from app.API.ResponseModels.Register import RegisterResponseSucces, RegisterResponseFail
from app.API.ResponseModels.Login import SuccesLogin
from .func import (login, login_by_token,
                   registration, delete_user)
from . import users

import pytest
import httpx


@pytest.mark.asyncio
@pytest.mark.parametrize("data", users)
async def test_regisration(client: httpx.AsyncClient, data: dict):
    status, response = await registration(client, data)

    assert status == 200 and RegisterResponseSucces(**response)
    
    index = users.index(data)
    users[index]["token"] = response["token"]

@pytest.mark.asyncio
@pytest.mark.parametrize("token", users)
async def test_login_by_token_success(client: httpx.AsyncClient, token: str):
    status, data = await login_by_token(client, token["token"])

    assert status == 200 and SuccesLogin(**data)

@pytest.mark.asyncio
@pytest.mark.parametrize("token", users)
async def test_delete_user_session(client: httpx.AsyncClient, token: str):
    cookie = {"token": token["token"]}

    request = await client.delete('/api/admin/delete/session/user',
                            cookies=cookie)
    
    assert request.status_code == 200

@pytest.mark.asyncio
@pytest.mark.parametrize("token", users)
async def test_login_by_token_fail(client: httpx.AsyncClient, token: str):
    status, _ = await login_by_token(client, token["token"])

    assert status == 500

@pytest.mark.asyncio
@pytest.mark.parametrize("data", users)
async def test_login_success(client: httpx.AsyncClient, data: dict):
    status, user = await login(client, data)

    assert status == 200 and RegisterResponseSucces(**user)

    index = users.index(data)
    users[index]["token"] = user["token"]

@pytest.mark.asyncio
@pytest.mark.parametrize("data", users)
async def test_login_fail(client: httpx.AsyncClient, data: dict):
    data['password'] = "".join([chr(ord(i) + 2) for i in data["password"]])

    status, user =  await login(client, data)

    assert status == 403 and RegisterResponseFail(**user)

@pytest.mark.asyncio
@pytest.mark.parametrize("data", users)
async def test_get_full_info_fail(client: httpx.AsyncClient, data: dict):
    cookie = {"token": data.get("token")}

    request = await client.get('/api/admin/get-full-info/user',
                         cookies=cookie)
    
    assert request.status_code == 500

@pytest.mark.asyncio
@pytest.mark.parametrize("data", users)
async def test_delete_user(client: httpx.AsyncClient, data: dict):
    status = await delete_user(client, data.get("token"))
    
    assert status == 200