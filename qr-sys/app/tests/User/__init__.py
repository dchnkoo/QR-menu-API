from random import randint


def set_user_data(email: str, password: str, type_time: str = "days", number: int = 1) -> dict:
    user_data_keys = ("email", "password", "time")

    data = dict(zip(user_data_keys, (email, password)))
    data["time"] = dict(zip(["type", "number"], [type_time, number]))

    return data

def chr_generate(*, a: int, b: int, rang: int) -> str:
    return "".join([chr(randint(a, b)) for _ in range(rang)])

def generate_email() -> str:
    name = chr_generate(a=65, b=90, rang=10).lower()

    return name + "@gmail.com"

def generate_password() -> str:
    return chr_generate(a=65, b=90, rang=25)


users = [set_user_data(generate_email(), generate_password()) for _ in range(4)]