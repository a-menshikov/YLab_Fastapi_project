from typing import Any

import pytest


@pytest.fixture
def menu_post() -> dict[str, str]:
    """Фикстура меню для POST."""
    return {
        'title': 'First menu',
        'description': 'Some description'
    }


@pytest.fixture
def menu_patch() -> dict[str, str]:
    """Фикстура меню для PATCH."""
    return {
        'title': 'First menu updated',
        'description': 'Some description updated'
    }


@pytest.fixture
def submenu_post() -> dict[str, str]:
    """Фикстура подменю для POST."""
    return {
        'title': 'First submenu',
        'description': 'Some description'
    }


@pytest.fixture
def submenu_patch() -> dict[str, str]:
    """Фикстура подменю для PATCH."""
    return {
        'title': 'First submenu updated',
        'description': 'Some description updated'
    }


@pytest.fixture
def dish_post() -> dict[str, str]:
    """Фикстура блюда для POST."""
    return {
        'title': 'First dish',
        'description': 'Some description',
        'price': '123.456',
    }


@pytest.fixture
def dish_2_post() -> dict[str, str]:
    """Фикстура второго блюда для POST."""
    return {
        'title': 'Second dish',
        'description': 'Some another description',
        'price': '654.123',
    }


@pytest.fixture
def dish_patch() -> dict[str, str]:
    """Фикстура блюда для PATCH."""
    return {
        'title': 'First dish updated',
        'description': 'Some description updated',
        'price': '654.123',
    }


@pytest.fixture(scope='module')
def saved_data() -> dict[str, Any]:
    """Фикстура дял сохранения объектов тестирования."""
    return {}
