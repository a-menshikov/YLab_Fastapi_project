from decimal import Decimal
from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from app.api.dishes.api import get_dishes, post_new_dish
from app.api.menus.api import destroy_menu, get_menu, get_menus, post_new_menu
from app.api.submenus.api import (
    destroy_submenu,
    get_submenu,
    get_submenus,
    post_new_submenu,
)
from tests.service import reverse


async def test_post_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового меню."""
    response = await client.post(
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


async def test_post_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового подменю."""
    menu = saved_data['menu']
    response = await client.post(
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


async def test_post_first_dish(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление первого нового блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(
            post_new_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id']
        ),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора блюда нет в ответе'
    assert 'submenu_id' in response.json(), \
        'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия блюда нет в ответе'
    assert 'description' in response.json(), 'Описания блюда нет в ответе'
    assert 'price' in response.json(), 'Цены блюда нет в ответе'
    assert response.json()['title'] == dish_post['title'], \
        'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish_post['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == str(Decimal(
        dish_post['price']).quantize(Decimal('0.00'))), \
        'Цена блюда не соответствует ожидаемой'

    saved_data['dish_1'] = response.json()


async def test_post_second_dish(
    dish_2_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление второго нового блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(
            post_new_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id']
        ),
        json=dish_2_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора блюда нет в ответе'
    assert 'submenu_id' in response.json(), \
        'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия блюда нет в ответе'
    assert 'description' in response.json(), 'Описания блюда нет в ответе'
    assert 'price' in response.json(), 'Цены блюда нет в ответе'
    assert response.json()['title'] == dish_2_post['title'], \
        'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish_2_post['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == str(Decimal(
        dish_2_post['price']).quantize(Decimal('0.00'))), \
        'Цена блюда не соответствует ожидаемой'

    saved_data['dish_2'] = response.json()


async def test_current_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение текущего меню."""
    menu = saved_data['menu']
    response = await client.get(
        reverse(get_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == menu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == menu['title'], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu['description'], \
        'Описание меню не соответствует ожидаемому'
    assert response.json()['submenus_count'] == 1, \
        'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 2, \
        'Количество блюд не соответствует ожидаемому'


async def test_get_currnet_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(
            get_submenu,
            menu_id=menu['id'],
            submenu_id=submenu['id']
        ),
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
    assert response.json()['dishes_count'] == 2, \
        'Количество блюд не соответствует ожидаемому'


async def test_delete_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse(
            destroy_submenu,
            menu_id=menu['id'],
            submenu_id=submenu['id']
        ),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"submenu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_submenu_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = await client.get(
        reverse(get_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_dish_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Проверка получения пустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(
            get_dishes,
            menu_id=menu['id'],
            submenu_id=submenu['id']
        ),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_current_menu_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение текущего меню c нулевым количеством подменю и блюд."""
    menu = saved_data['menu']
    response = await client.get(
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


async def test_delete_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = await client.delete(
        reverse(destroy_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_all_menu_empty(client: AsyncClient) -> None:
    """Проверка получения пустого списка меню."""
    response = await client.get(
        reverse(get_menus),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'
