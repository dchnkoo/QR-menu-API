async def registration(client, data: dict):
    request = await client.post('/api/admin/register', 
                            json=data)
    
    response = request.json()
    return request.status_code, response

async def login_by_token(client, token: str):
    cookie = {"token": token}

    request = await client.get('/api/admin/login/token', 
                         cookies=cookie)
    
    return request.status_code, request.json()

async def login(client, data: dict):
    request = await client.post('/api/admin/login', json=data)

    return request.status_code, request.json()

async def delete_user(client, token) -> int:
    request = await client.delete("/api/admin/delete/user", 
                            cookies={"token": token})
    
    return request.status_code