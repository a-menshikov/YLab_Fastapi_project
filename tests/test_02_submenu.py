from http import HTTPStatus
from typing import Any

from app.api.menus.api import destroy_menu, post_new_menu
from app.api.submenus.api import (
    destroy_submenu,
    get_submenu,
    get_submenus,
    patch_submenu,
    post_new_submenu,
)
from tests.conftest import client
from tests.service import reverse


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

    saved_data['menu'] = response.json()


def test_submenu_empty(saved_data: dict[str, Any]) -> None:
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_post_submenu(submenu_post: dict[str, str],
                      saved_data: dict[str, Any]) -> None:
    """Добавление нового подменю."""
    menu = saved_data['menu']
    response = client.post(
        reverse(post_new_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
    assert 'menu_id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия подменю нет в ответе'
    assert 'description' in response.json(), 'Описания подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == submenu_post['title'], \
        'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu_post['description'], \
        'Описание подменю не соответствует ожидаемому'

    saved_data['submenu'] = response.json()


def test_post_submenu_double(submenu_post: dict[str, str],
                             saved_data: dict[str, Any]) -> None:
    """Добавление нового подменю с одинаковым названием."""
    menu = saved_data['menu']
    response = client.post(
        reverse(post_new_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, \
        'Статус ответа не 400'


def test_all_submenu_not_empty(saved_data: dict[str, Any]) -> None:
    """Проверка получения непустого списка подменю."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


def test_get_posted_submenu(saved_data: dict[str, Any]) -> None:
    """Получение созданного подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == submenu['id'], \
        'Идентификатор подменю не соответствует ожидаемому'
    assert response.json()['menu_id'] == menu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == submenu['title'], \
        'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu['description'], \
        'Описание подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, \
        'Количество блюд не соответствует ожидаемому'


def test_patch_submenu(submenu_patch: dict[str, str],
                       saved_data: dict[str, Any]) -> None:
    """Изменение текущего меню."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.patch(
        reverse(patch_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
        json=submenu_patch,
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
    assert 'menu_id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия подменю нет в ответе'
    assert 'description' in response.json(), 'Описания подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == submenu_patch['title'], \
        'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu_patch['description'], \
        'Описание подменю не соответствует ожидаемому'

    saved_data['submenu'] = response.json()


def test_get_patched_submenu(saved_data: dict[str, Any]) -> None:
    """Получение обновленного подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == submenu['id'], \
        'Идентификатор подменю не соответствует ожидаемому'
    assert response.json()['menu_id'] == menu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == submenu['title'], \
        'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu['description'], \
        'Описание подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, \
        'Количество блюд не соответствует ожидаемому'


def test_delete_submenu(saved_data: dict[str, Any]) -> None:
    """Удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.delete(
        reverse(destroy_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"submenu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_submenu_empty_after_delete(saved_data: dict[str, Any]) -> None:
    """Проверка получения пустого списка подменю после удаления."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_get_deleted_submenu(saved_data: dict[str, Any]) -> None:
    """Получение удаленного подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'submenu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'


def test_delete_menu(saved_data: dict[str, Any]) -> None:
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = client.delete(
        reverse(destroy_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_deleted_menu_submenu_empty(saved_data: dict[str, Any]) -> None:
    """Проверка получения пустого списка подменю у несуществующего меню."""
    menu = saved_data['menu']
    response = client.get(
        reverse(get_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_post_objects_for_cascade_check(menu_post: dict[str, str],
                                        submenu_post: dict[str, str],
                                        saved_data: dict[str, Any]) -> None:
    """Добавление нового меню и подменю для последующей проверки
    каскадного удаления."""
    response = client.post(
        reverse(post_new_menu),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'

    saved_data['menu'] = response.json()

    menu = saved_data['menu']
    response = client.post(
        reverse(post_new_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'

    saved_data['submenu'] = response.json()


def test_delete_menu_for_cascade_check(saved_data: dict[str, Any]) -> None:
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = client.delete(
        reverse(destroy_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_get_deleted_submenu_cascade_check(saved_data: dict[str, Any]) -> None:
    """Получение подменю удаленного меню, проверка каскадного удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'submenu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'
