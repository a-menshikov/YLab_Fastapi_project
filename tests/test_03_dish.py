from decimal import Decimal
from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from app.api.dishes.api import (
    destroy_dish,
    get_dish,
    get_dishes,
    patch_dish,
    post_new_dish,
)
from app.api.menus.api import destroy_menu, post_new_menu
from app.api.submenus.api import destroy_submenu, post_new_submenu
from tests.service import reverse


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


async def test_dish_empty(saved_data: dict[str, Any],
                          client: AsyncClient) -> None:
    """Проверка получения пустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_dish(dish_post: dict[str, str],
                         saved_data: dict[str, Any],
                         client: AsyncClient) -> None:
    """Добавление нового блюда."""
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


async def test_post_dish_double(dish_post: dict[str, str],
                                saved_data: dict[str, Any],
                                client: AsyncClient) -> None:
    """Добавление нового блюда с одинаковым названием и описанием."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(post_new_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, \
        'Статус ответа не 400'


async def test_dish_not_empty(saved_data: dict[str, Any],
                              client: AsyncClient) -> None:
    """Проверка получения непустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_get_posted_dish(saved_data: dict[str, Any],
                               client: AsyncClient) -> None:
    """Получение созданного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == dish['id'], \
        'Идентификатор блюда не соответствует ожидаемому'
    assert response.json()['submenu_id'] == submenu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == dish['title'], \
        'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == dish['price'], \
        'Ццна блюда не соответствует ожидаемой'


async def test_patch_dish(dish_patch: dict[str, str],
                          saved_data: dict[str, Any],
                          client: AsyncClient) -> None:
    """Изменение текущего блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.patch(
        reverse(patch_dish, menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id']),
        json=dish_patch,
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора блюда нет в ответе'
    assert 'submenu_id' in response.json(), \
        'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия блюда нет в ответе'
    assert 'description' in response.json(), 'Описания блюда нет в ответе'
    assert 'price' in response.json(), 'Цены блюда нет в ответе'
    assert response.json()['title'] == dish_patch['title'], \
        'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish_patch['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == str(Decimal(
        dish_patch['price']).quantize(Decimal('0.00'))), \
        'Цена блюда не соответствует ожидаемой'

    saved_data['dish'] = response.json()


async def test_get_patched_dish(saved_data: dict[str, Any],
                                client: AsyncClient) -> None:
    """Получение обновленного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == dish['id'], \
        'Идентификатор блюда не соответствует ожидаемому'
    assert response.json()['submenu_id'] == submenu['id'], \
        'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == dish['title'], \
        'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == dish['price'], \
        'Ццна блюда не соответствует ожидаемой'


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


async def test_dish_empty_after_delete(saved_data: dict[str, Any],
                                       client: AsyncClient) -> None:
    """Проверка получения пустого списка блюд после удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_get_deleted_dish(saved_data: dict[str, Any],
                                client: AsyncClient) -> None:
    """Получение удаленного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', \
        'Сообщение об ошибке не соответствует ожидаемому'


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


async def test_deleted_submenu_dish_empty(saved_data: dict[str, Any],
                                          client: AsyncClient) -> None:
    """Проверка получения пустого списка блюд у несуществующего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_objects_for_cascade_chek(submenu_post: dict[str, str],
                                             dish_post: dict[str, str],
                                             saved_data: dict[str, Any],
                                             client: AsyncClient) -> None:
    """Добавление нового подменю и блюда для проверки каскадного удаления."""
    menu = saved_data['menu']
    response = await client.post(
        reverse(post_new_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'

    saved_data['submenu'] = response.json()

    submenu = saved_data['submenu']
    response = await client.post(
        reverse(post_new_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'

    saved_data['dish'] = response.json()


async def test_delete_submenu_for_cascade_chek(saved_data: dict[str, Any],
                                               client: AsyncClient) -> None:
    """Удаление текущего подменю для проверки каскадного удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse(destroy_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"submenu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_get_deleted_dish_cascade_chek(saved_data: dict[str, Any],
                                             client: AsyncClient) -> None:
    """Получение удаленного блюда, проверка каскадного удаления.."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', \
        'Сообщение об ошибке не соответствует ожидаемому'


async def test_delete_menu_finally(saved_data: dict[str, Any],
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
