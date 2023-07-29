from http import HTTPStatus

from tests.conftest import client


def test_all_menu_empty():
    """Проверка получения пустого списка меню."""
    response = client.get(
        "/api/v1/menus/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_post_menu(menu_post, saved_data):
    """Добавление нового меню."""
    response = client.post(
        "/api/v1/menus/",
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), \
        'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == menu_post['title'], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu_post['description'], \
        'Описание меню не соответствует ожидаемому'

    saved_data['menu'] = response.json()


def test_post_menu_double(menu_post):
    """Добавление нового меню с одинаковым названием."""
    response = client.post(
        "/api/v1/menus/",
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, \
        'Статус ответа не 400'


def test_all_menu_not_empty():
    """Проверка получения непустого списка меню."""
    response = client.get(
        "/api/v1/menus/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


def test_get_posted_menu(saved_data):
    """Получение созданного меню."""
    menu = saved_data['menu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == menu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == menu['title'], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu['description'], \
        'Описание меню не соответствует ожидаемому'
    assert response.json()['submenus_count'] == 0, \
        'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, \
        'Количество блюд не соответствует ожидаемому'


def test_patch_menu(menu_patch, saved_data):
    """Изменение текущего меню."""
    menu = saved_data['menu']
    response = client.patch(
        f"/api/v1/menus/{menu['id']}",
        json=menu_patch,
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), \
        'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == menu_patch['title'], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu_patch['description'], \
        'Описание меню не соответствует ожидаемому'

    saved_data['menu'] = response.json()


def test_get_patched_menu(saved_data):
    """Получение обновленного меню."""
    menu = saved_data['menu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == menu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == menu['title'], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu['description'], \
        'Описание меню не соответствует ожидаемому'
    assert response.json()['submenus_count'] == 0, \
        'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, \
        'Количество блюд не соответствует ожидаемому'


def test_delete_menu(saved_data):
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = client.delete(
        f"/api/v1/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_get_deleted_menu(saved_data):
    """Получение удаленного меню."""
    menu = saved_data['menu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'menu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'
