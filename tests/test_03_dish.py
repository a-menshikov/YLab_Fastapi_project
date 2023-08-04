from decimal import Decimal
from http import HTTPStatus

from tests.conftest import client


def test_post_menu(menu_post, saved_data):
    """Добавление нового меню."""
    response = client.post(
        '/api/v1/menus/',
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


def test_post_submenu(submenu_post, saved_data):
    """Добавление нового подменю."""
    menu = saved_data['menu']
    response = client.post(
        f"/api/v1/menus/{menu['id']}/submenus/",
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


def test_dish_empty(saved_data):
    """Проверка получения пустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_post_dish(dish_post, saved_data):
    """Добавление нового блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.post(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
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


def test_post_dish_double(dish_post, saved_data):
    """Добавление нового блюда с одинаковым названием и описанием."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.post(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, \
        'Статус ответа не 400'


def test_dish_not_empty(saved_data):
    """Проверка получения непустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


def test_get_posted_dish(saved_data):
    """Получение созданного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/"
        f"dishes/{dish['id']}",
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


def test_patch_dish(dish_patch, saved_data):
    """Изменение текущего блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.patch(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/"
        f"dishes/{dish['id']}",
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


def test_get_patched_dish(saved_data):
    """Получение обновленного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/"
        f"dishes/{dish['id']}",
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


def test_delete_dish(saved_data):
    """Удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.delete(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/"
        f"dishes/{dish['id']}",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"dish deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_dish_empty_after_delete(saved_data):
    """Проверка получения пустого списка блюд после удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_get_deleted_dish(saved_data):
    """Получение удаленного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/"
        f"dishes/{dish['id']}",
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', \
        'Сообщение об ошибке не соответствует ожидаемому'


def test_delete_submenu(saved_data):
    """Удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.delete(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"submenu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_deleted_submenu_dish_empty(saved_data):
    """Проверка получения пустого списка блюд у несуществующего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_post_submenu_and_dish_for_cascade_chek(submenu_post, dish_post,
                                                saved_data):
    """Добавление нового подменю и блюда для проверки каскадного удаления."""
    menu = saved_data['menu']
    response = client.post(
        f"/api/v1/menus/{menu['id']}/submenus/",
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'

    saved_data['submenu'] = response.json()

    submenu = saved_data['submenu']
    response = client.post(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'

    saved_data['dish'] = response.json()


def test_delete_submenu_for_cascade_chek(saved_data):
    """Удаление текущего подменю для проверки каскадного удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.delete(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"submenu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'


def test_get_deleted_dish_cascade_chek(saved_data):
    """Получение удаленного блюда, проверка каскадного удаления.."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/"
        f"dishes/{dish['id']}",
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', \
        'Сообщение об ошибке не соответствует ожидаемому'


def test_delete_menu_finally(saved_data):
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = client.delete(
        f"/api/v1/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.text == '"menu deleted"', \
        'Сообщение об удалении не соответствует ожидаемому'
