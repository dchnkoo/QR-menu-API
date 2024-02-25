import re, os
from app.settings import (DEBUG, REDIS_PORT, REDIS_PASSWORD,
                          DATABASE)


if not DEBUG:
    raise Exception("Set DEBUG=True for no production enviroment")

# Виявлення операційної системи
your_os = os.name == "posix"

path = lambda x: f"{x}".join(os.path.abspath(__file__).split(f"{x}")[:-1])

cmd_path = path("/") if your_os else path("\\")
cmd = os.system

# Встановлення середовища для виконання команд
os.chdir(cmd_path)

# Встановлення залежностей проекту
pip = "pip3" if your_os else "pip"
cmd(f"{pip} install -r requirements.txt")


# Запуск контейнеру redis
cmd(f"docker run --name re --rm -d -p {REDIS_PORT}:6379 redis --requirepass {REDIS_PASSWORD}")

# Запуск контейнеру postgres
user, password, port, db = re.search(r":\/\/([A-z0-9]+):([A-z0-9]+)@[A-z0-9]+:(\d+)\/([A-z0-9]+)$", DATABASE).groups()
cmd(f"docker run --name db --rm -d -p {port}:5432 -e POSTGRES_USER={user} -e POSTGRES_DB={db} -e POSTGRES_PASSWORD={password} postgres")

# Чекаємо ініціалізацію БД
cmd("sleep 10" if your_os else "timeout /t 10")

cmd("alembic revision --autogenerate")
cmd("alembic upgrade head")

python = "python3" if your_os else "python"

# Генерація секретного ключа 
cmd(f"{python} -m app.SECRET_KEY.generate --set-secret")

cmd("sleep 2" if your_os else "timeout /t 2")

cmd(f"{python} -m app.tests.run start")

cmd("uvicorn app.API.api:app --reload")