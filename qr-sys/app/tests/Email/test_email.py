import pytest
import httpx


keys = ("email_to", "theme", "body")

@pytest.mark.asyncio
@pytest.mark.parametrize("data", [dict(zip(keys, ("example@gmail.com", "test", "test"))) for _ in range(5)])
async def test_send_mail(client: httpx.AsyncClient, data: dict, event_loop_policy):
    request = await client.post("/api/admin/send_email", json=data)

    assert request.status_code == 200 and ("msg" in request.json()) is True

