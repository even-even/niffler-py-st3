from json import JSONDecodeError

import httpx
from curlify2 import Curlify
from loguru import logger

from tests.src.allure_decorators import Step


class BaseApiRequest:
    """Базовый класс для выполнения HTTP-запросов."""

    def __init__(self, api_key: str | None = "reqres-free-v1") -> None:
        """Конструктор класса, устанавливает базовые параметры для выполнения запросов.

        :param api_key: Обязательный хедер
        """
        self.api_key = api_key

    def request(self, method: str, url: str, path: str, *, headers: dict[str, str] | None = None,  # noqa: PLR0913
                params: dict | None = None, data: dict | None = None, json: dict | None = None,
                files: dict | None = None) -> httpx.Response:
        """Общий метод для выполнения HTTP-запросов.

        :param method: Метод HTTP-запроса (GET, POST, PUT, PATCH, DELETE).
        :param url: Базовый URL для выполнения запроса.
        :param path: Путь к ресурсу на сервере.
        :param headers: Дополнительные заголовки запроса.
        :param params: Параметры запроса (для GET-запросов).
        :param data: Тело запроса (для POST/PUT/PATCH-запросов).
        :param json: JSON-тело запроса (для POST/PUT/PATCH-запросов).
        :param files: Файлы для отправки (для POST-запросов).
        :return: Объект httpx.Response с результатом запроса.
        """
        final_headers = headers.copy() if headers else {}
        if self.api_key:
            final_headers["x-api-key"] = self.api_key

        full_url = f"{url}{path}"

        with Step(f"Выполнить {method.upper()} запрос {full_url}"):
            kwargs_to_pass = {
                "headers": final_headers,
                "params": params or {},
                "verify": False,
                "timeout": (45, 45),
            }

            if method.lower() in ("post", "put", "patch"):
                kwargs_to_pass.update({
                    "json": json,
                    "data": data,
                })

            if method.lower() == "post":
                kwargs_to_pass["files"] = files

            # Выполнение запроса
            result = getattr(httpx, method.lower())(
                url=full_url, **kwargs_to_pass)

            # Логирование ответа
            _log_request_result(result)

            return result

    def get(self, url: str, path: str, params: dict | None = None) -> httpx.Response:
        """Выполнить GET запрос"""
        return self.request(method="GET", url=url, path=path, params=params)

    def post(self, url: str, path: str, params: dict | None = None, data: dict | None = None,  # noqa: PLR0917, PLR0913
             json: dict | None = None, files: dict | None = None) -> httpx.Response:
        """Выполнить POST запрос"""
        return self.request(
            method="POST", url=url, path=path, params=params, data=data, json=json, files=files)

    def patch(self, url: str, path: str, data: dict | None = None, json: dict | None = None,
              params: dict | None = None) -> httpx.Response:
        """Выполнить PATCH запрос"""
        return self.request(method="PATCH", url=url, path=path, data=data, json=json, params=params)

    def put(self, url: str, path: str, data: dict | None = None, json: dict | None = None) -> httpx.Response:
        """Выполнить PUT запрос"""
        return self.request(method="PUT", url=url, path=path, data=data, json=json)

    def delete(self, url: str, path: str, params: dict | None = None) -> httpx.Response:
        """Выполнить DELETE запрос"""
        return self.request(method="DELETE", url=url, path=path, params=params)


def _log_request_result(response: httpx.Response) -> None:
    """Логируем информацию о запросе/ответе"""
    request_message = f"\n\t|> Запрос:\n\t{Curlify(response.request).to_curl()}\n\t"

    try:
        log_msg = (
            f"{request_message}"
            f"|> Ответ:\n\t{str(response.json())[:1500]}\n\t"
            f"|> Статус-код: {response.status_code}"
        )
        logger.info(log_msg)
    except JSONDecodeError:
        log_msg = (
            f"{request_message}"
            f"|> Ответ: {response.text}\n\t"
            f"|> Статус-код: {response.status_code}"
        )
        logger.info(log_msg)
