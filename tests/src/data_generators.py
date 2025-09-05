import random
import string


def get_random_string(length: int = 6, is_numbers: bool = True) -> str:
    """Получение рандомной строки"""
    symbols = string.ascii_letters + string.digits if not is_numbers else string.ascii_letters
    return "".join(random.choices(symbols, k=length))


def get_random_russian_string(length: int = 1) -> str:
    """Получение рандомной строки с русскими символами"""
    return "".join(random.choice(tuple("авекмнорстух")) for _ in range(length))


def get_random_number(length: int = 10) -> str:
    """Получение рандомного числа int"""
    result = "".join(random.choices(string.digits, k=length))
    if result[0] == "0":
        result = result.replace(result[0], "1")
    return result


def get_random_phone_number() -> str:
    """Получение рандомного номера телефона +79ххххххххх"""
    return f"+79{''.join(random.choice(string.digits) for _ in range(9))}"


def get_random_email() -> str:
    """Получение рандомной электронной почты @autotest.ru"""
    return f"autotest_{''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(6))}@autotest.ru"
