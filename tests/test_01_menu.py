from http import HTTPStatus
from typing import Any

from app.api.menus.api import (
    destroy_menu,
    get_menu,
    get_menus,
    patch_menu,
    post_new_menu,
)
from tests.conftest import client
from tests.service import reverse


def test_all_menu_empty() -> None:
    """Проверка получения пустого списка меню."""
    response = client.get(
        reverse(get_menus),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_post_menu(menu_post: dict[str, str],
                   saved_data: dict[str, Any]) -> None:
    """Добавление нового меню."""
    response = client.post(
        reverse(post_new_menu),
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


def test_post_menu_double(menu_post: dict[str, str]) -> None:
    """Добавление нового меню с одинаковым названием."""
    response = client.post(
        reverse(post_new_menu),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, \
        'Статус ответа не 400'


def test_all_menu_not_empty() -> None:
    """Проверка получения непустого списка меню."""
    response = client.get(
        reverse(get_menus),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


def test_get_posted_menu(saved_data) -> None:
    """Получение созданного меню."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_menu, menu_id=menu['id']),
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


def test_patch_menu(menu_patch: dict[str, str], saved_data) -> None:
    """Изменение текущего меню."""
    menu = saved_data['menu']
    response = client.patch(
        reverse(patch_menu, menu_id=menu['id']),
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


def test_get_patched_menu(saved_data) -> None:
    """Получение обновленного меню."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_menu, menu_id=menu['id']),
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


def test_delete_menu(saved_data) -> None:
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = client.delete(
        reverse(destroy_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_get_deleted_menu(saved_data) -> None:
    """Получение удаленного меню."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'menu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'
