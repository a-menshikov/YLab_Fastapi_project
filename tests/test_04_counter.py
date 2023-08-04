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


def test_post_first_dish(dish_post, saved_data):
    """Добавление первого нового блюда."""
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

    saved_data['dish_1'] = response.json()


def test_post_second_dish(dish_2_post, saved_data):
    """Добавление второго нового блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.post(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/",
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


def test_current_menu(saved_data):
    """Получение текущего меню."""
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
    assert response.json()['submenus_count'] == 1, \
        'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 2, \
        'Количество блюд не соответствует ожидаемому'


def test_get_currnet_submenu(saved_data):
    """Получение текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}",
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


def test_submenu_empty(saved_data):
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = client.get(
        f"/api/v1/menus/{menu['id']}/submenus/",
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


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


def test_current_menu_empty(saved_data):
    """Получение текущего меню c нулевым количеством подменю и блюд."""
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


def test_all_menu_empty():
    """Проверка получения пустого списка меню."""
    response = client.get(
        '/api/v1/menus/',
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'
