from ...settings import COOKIE_KEY
import httpx

async def registration(client: httpx.AsyncClient, data: dict):
    request = await client.post('/api/admin/register', 
                            json=data)

    response = request.json()
    return request.status_code, response, request.cookies.get(COOKIE_KEY)

async def login_by_token(client, token: str):
    cookie = {COOKIE_KEY: token}

    request = await client.get('/api/admin/login/token', 
                         cookies=cookie)
    
    return request.status_code, request.json()

async def login(client, data: dict):
    request = await client.post('/api/admin/login', json=data)

    return request.status_code, request.json(), request.cookies

async def delete_user(client, token) -> int:
    request = await client.delete("/api/admin/delete/user", 
                            cookies={COOKIE_KEY: token})
    
    return request.status_code