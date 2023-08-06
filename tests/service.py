from typing import Callable

from app.main import app


def get_routes() -> dict[str, str]:
    """Получение словаря с маршрутами приложения."""
    routes = {}
    for route in app.routes:
        routes[route.endpoint.__name__] = route.path
    return routes


def reverse(foo: Callable, routes: dict[str, str] = get_routes(),
            **kwargs) -> str:
    """Получение url по маршруту."""
    path = routes[foo.__name__]
    return path.format(**kwargs)
