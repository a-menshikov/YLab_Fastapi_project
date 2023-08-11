from decimal import Decimal
from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from app.api.dishes.api import destroy_dish, post_new_dish
from app.api.menus.api import destroy_menu, get_full_base_menu, post_new_menu
from app.api.submenus.api import destroy_submenu, post_new_submenu
from tests.service import reverse


async def test_all_menu_empty(client: AsyncClient) -> None:
    """Проверка получения пустого списка меню."""
    response = await client.get(
        reverse(get_full_base_menu),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_menu(menu_post: dict[str, str],
                         saved_data: dict[str, Any],
                         client: AsyncClient) -> None:
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


async def test_post_submenu(submenu_post: dict[str, str],
                            saved_data: dict[str, Any],
                            client: AsyncClient) -> None:
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


async def test_post_dish(dish_post: dict[str, str],
                         saved_data: dict[str, Any],
                         client: AsyncClient) -> None:
    """Добавление первого нового блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(post_new_dish, menu_id=menu['id'], submenu_id=submenu['id']),
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

    saved_data['dish'] = response.json()


async def test_full_base(menu_post: dict[str, str],
                         submenu_post: dict[str, str],
                         dish_post: dict[str, str],
                         saved_data: dict[str, Any],
                         client: AsyncClient) -> None:
    """Проверка полного вывода базы."""
    response = await client.get(
        reverse(get_full_base_menu),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'

    data = response.json()

    assert len(data) == 1, 'В ответе не одно меню'
    assert data[0]['title'] == menu_post['title'], \
        'Название меню не соответствует ожидаемому'
    assert data[0]['description'] == menu_post['description'], \
        'Описание меню не соответствует ожидаемому'
    assert data[0]['id'] == saved_data['menu']['id'], \
        'Идентификатора меню не соответствует ожидаемому'
    assert len(data[0]['submenus']) == 1, \
        'Количество подменю не соответствует ожидаемому'

    submenu = data[0]['submenus'][0]

    assert submenu['title'] == submenu_post['title'], \
        'Название подменю не соответствует ожидаемому'
    assert submenu['description'] == submenu_post['description'], \
        'Описание подменю не соответствует ожидаемому'
    assert submenu['id'] == saved_data['submenu']['id'], \
        'Идентификатора подменю не соответствует ожидаемому'
    assert len(submenu['dishes']) == 1, \
        'Количество блюд не соответствует ожидаемому'

    dish = submenu['dishes'][0]

    assert dish['title'] == dish_post['title'], \
        'Название блюда не соответствует ожидаемому'
    assert dish['description'] == dish_post['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert dish['price'] == str(Decimal(
        dish_post['price']).quantize(Decimal('0.00'))), \
        'Цена блюда не соответствует ожидаемой'
    assert dish['id'] == saved_data['dish']['id'], \
        'Идентификатора блюда не соответствует ожидаемому'


async def test_delete_dish(saved_data: dict[str, Any],
                           client: AsyncClient) -> None:
    """Удаление текущего блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.delete(
        reverse(destroy_dish, menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"dish deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_full_base_after_dish_dete(menu_post: dict[str, str],
                                         submenu_post: dict[str, str],
                                         saved_data: dict[str, Any],
                                         client: AsyncClient) -> None:
    """Проверка полного вывода базы после удаления блюда."""
    response = await client.get(
        reverse(get_full_base_menu),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'

    data = response.json()

    assert len(data) == 1, 'В ответе не одно меню'
    assert data[0]['title'] == menu_post['title'], \
        'Название меню не соответствует ожидаемому'
    assert data[0]['description'] == menu_post['description'], \
        'Описание меню не соответствует ожидаемому'
    assert data[0]['id'] == saved_data['menu']['id'], \
        'Идентификатора меню не соответствует ожидаемому'
    assert len(data[0]['submenus']) == 1, \
        'Количество подменю не соответствует ожидаемому'

    submenu = data[0]['submenus'][0]

    assert submenu['title'] == submenu_post['title'], \
        'Название подменю не соответствует ожидаемому'
    assert submenu['description'] == submenu_post['description'], \
        'Описание подменю не соответствует ожидаемому'
    assert submenu['id'] == saved_data['submenu']['id'], \
        'Идентификатора подменю не соответствует ожидаемому'
    assert len(submenu['dishes']) == 0, \
        'Количество блюд не соответствует ожидаемому'


async def test_delete_submenu(saved_data: dict[str, Any],
                              client: AsyncClient) -> None:
    """Удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse(destroy_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"submenu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_full_base_after_submenu_dete(menu_post: dict[str, str],
                                            saved_data: dict[str, Any],
                                            client: AsyncClient) -> None:
    """Проверка полного вывода базы после удаления блюда."""
    response = await client.get(
        reverse(get_full_base_menu),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'

    data = response.json()

    assert len(data) == 1, 'В ответе не одно меню'
    assert data[0]['title'] == menu_post['title'], \
        'Название меню не соответствует ожидаемому'
    assert data[0]['description'] == menu_post['description'], \
        'Описание меню не соответствует ожидаемому'
    assert data[0]['id'] == saved_data['menu']['id'], \
        'Идентификатора меню не соответствует ожидаемому'
    assert len(data[0]['submenus']) == 0, \
        'Количество подменю не соответствует ожидаемому'


async def test_delete_menu(saved_data: dict[str, Any],
                           client: AsyncClient) -> None:
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = await client.delete(
        reverse(destroy_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_full_base_after_menu_dete(client: AsyncClient) -> None:
    """Проверка полного вывода базы после удаления меню."""
    response = await client.get(
        reverse(get_full_base_menu),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'
