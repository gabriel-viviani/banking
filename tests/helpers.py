from decimal import Decimal
from datetime import Date
import random
import Faker


def random_valid_cpf() -> str:
    cpf = [random.randint(0, 9) for x in range(9)]
    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
        cpf.append(11 - val if val > 1 else 0)
    return "".join(str(n) for n in cpf)


def random_name() -> str:
    name: str = Faker().name()
    return name


def random_int() -> int:
    x: int = Faker().random_int()
    return x


def random_decimal() -> Decimal:
    x: Decimal = Faker().random_decimal()
    return x


def rand_date() -> Date:
    x: Date = Faker().date()
    return x
