import os
import argparse

parser = argparse.ArgumentParser(description="Запуск тестів")



def start_tests():
    test_modules = ["User", "Restaurant", "Category",
                    "Dishes", "Ingredients", "Tables", "Email"]

    to_dir = "/".join(os.path.abspath(__file__).split("/")[:-1])
    [os.system(f"pytest {to_dir}/{i} -p no:warnings") for i in test_modules]

parser.add_argument("start", action=start_tests())