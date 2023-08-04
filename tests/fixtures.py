import pytest


@pytest.fixture
def menu_post():
    """Фикстура меню для POST."""
    return {
        'title': 'First menu',
        'description': 'Some description'
    }


@pytest.fixture
def menu_patch():
    """Фикстура меню для PATCH."""
    return {
        'title': 'First menu updated',
        'description': 'Some description updated'
    }


@pytest.fixture
def submenu_post():
    """Фикстура подменю для POST."""
    return {
        'title': 'First submenu',
        'description': 'Some description'
    }


@pytest.fixture
def submenu_patch():
    """Фикстура подменю для PATCH."""
    return {
        'title': 'First submenu updated',
        'description': 'Some description updated'
    }


@pytest.fixture
def dish_post():
    """Фикстура блюда для POST."""
    return {
        'title': 'First dish',
        'description': 'Some description',
        'price': '123.456',
    }


@pytest.fixture
def dish_2_post():
    """Фикстура второго блюда для POST."""
    return {
        'title': 'Second dish',
        'description': 'Some another description',
        'price': '654.123',
    }


@pytest.fixture
def dish_patch():
    """Фикстура блюда для PATCH."""
    return {
        'title': 'First dish updated',
        'description': 'Some description updated',
        'price': '654.123',
    }


@pytest.fixture(scope='module')
def saved_data():
    """Фикстура дял сохранения объектов тестирования."""
    return {}
