from app.API.ResponseModels.Register import RegisterResponseFail
from app.API.ResponseModels.Login import SuccesLogin

from .func import (login, login_by_token,
                   registration, delete_user)
from . import users

import pytest, pytest_asyncio
import httpx


@pytest_asyncio.fixture(scope="module", params=users)
async def register(client: httpx.AsyncClient, request):
    user = request.param

    status, response, token = await registration(client, user)

    assert status == 200 and RegisterResponseFail(**response)

    yield token, user

    status = await delete_user(client, token)
    
    assert status == 200

@pytest.mark.asyncio
async def test_login_by_token_fail(client: httpx.AsyncClient):
    status, _ = await login_by_token(client, "oueqwbfuoeqb")

    assert status == 401

@pytest.mark.asyncio
async def test_login_by_token_success(client: httpx.AsyncClient, register: str):
    status, data = await login_by_token(client, register[0])

    assert status == 200 and SuccesLogin(**data)

@pytest.mark.asyncio
async def test_delete_user_session(client: httpx.AsyncClient, register: str):
    cookie = {"token": register[0]}

    request = await client.delete('/api/admin/delete/session/user',
                            cookies=cookie)
    
    assert request.status_code == 200


@pytest.mark.asyncio
async def test_login_success(client: httpx.AsyncClient, register: tuple):
    status, user, _ = await login(client, register[1])

    assert status == 200 and RegisterResponseFail(**user)

@pytest.mark.asyncio
async def test_login_fail(client: httpx.AsyncClient, register: tuple):
    data = register[1]

    data['password'] = "".join([chr(ord(i) + 2) for i in data["password"]])

    status, user, _ =  await login(client, data)

    assert status == 403

@pytest.mark.asyncio
async def test_get_full_info_fail(client: httpx.AsyncClient, register: tuple):
    cookie = {"token": register[0]}

    request = await client.get('/api/admin/get-full-info/user',
                         cookies=cookie)
    
    assert request.status_code == 400

