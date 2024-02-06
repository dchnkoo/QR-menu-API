
async def add_category(client, token: str, data: dict = None, cookies: bool = True, loop = None):
    cookie = {"token": token} if cookies else None

    request = await client.post("/api/admin/add/category", cookies=cookie, json=data)

    return request.status_code, request.json()


async def delete_category(client, token: str, data: dict = None, cookies: bool = True, loop = None):
    cookie = {"token": token} if cookies else None

    args = "".join([f"{k}={v}&" for k, v in data.items()])[:-1]

    request = await client.delete("/api/admin/delete/categories?" + args, cookies=cookie)

    return request.status_code, request.json()