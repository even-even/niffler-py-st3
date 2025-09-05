from httpx import Response


def check_status_code(response: Response, status_code: int) -> None:
    """Проверка кода ответа с выводом тела в случае неуспеха"""
    assert response.status_code == status_code, (f"Ожидался status_code = {status_code},"
                                                 f" получен - {response} с текстом {response.text}")


def check_not_status_code_in_list(response: Response, status_code: tuple | int) -> None:
    """Проверка отсутствия кода ответа в blacklist"""
    if isinstance(status_code, int):
        status_code = (status_code,)
    msg = (f"status_code {response.status_code} = среди запрещенных {status_code},\n"
           f" получен - {response} с текстом {response.text}")
    assert response.status_code not in status_code, msg
