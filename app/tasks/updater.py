import requests

from app.config import (
    DISH_LINK,
    DISHES_LINK,
    MENU_LINK,
    MENUS_LINK,
    PREFIX_LINK,
    SUBMENU_LINK,
    SUBMENUS_LINK,
)


class BaseUpdaterRepo():
    """Сервисный репозиторий для обновления данных
    в базе после парсинга файла."""

    def __init__(self, parser_data: list[dict]):
        self.parser_data = parser_data

    def get_menus_from_db(self) -> list[str]:
        """Получить список id всех существующих меню из базы."""
        url = PREFIX_LINK + MENUS_LINK
        response = requests.get(url).json()
        menus_id = []
        for i in response:
            menus_id.append(i['id'])
        return menus_id

    def get_submenus_from_db(self, menu_id: str) -> list[str]:
        """Получить список id всех существующих подменю из базы."""
        url = PREFIX_LINK + SUBMENUS_LINK.format(menu_id=menu_id)
        response = requests.get(url).json()
        submenus_id = []
        for i in response:
            submenus_id.append(i['id'])
        return submenus_id

    def get_dishes_from_db(self, menu_id: str, submenu_id: str) -> list[str]:
        """Получить список id всех существующих блюд из базы."""
        url = PREFIX_LINK + DISHES_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        response = requests.get(url).json()
        dishes_id = []
        for i in response:
            dishes_id.append(i['id'])
        return dishes_id

    def post_menu(self, menu: dict[str, str | list]) -> None:
        """Запостить новое меню в базу."""
        url = PREFIX_LINK + MENUS_LINK
        data = {
            'id': menu['id'],
            'title': menu['title'],
            'description': menu['description'],
        }
        requests.post(url, json=data)

    def post_submenu(
        self,
        submenu: dict[str, str | list],
        menu_id: str,
    ) -> None:
        """Запостить новое подменю в базу."""
        url = PREFIX_LINK + SUBMENUS_LINK.format(menu_id=menu_id)
        data = {
            'id': submenu['id'],
            'title': submenu['title'],
            'description': submenu['description'],
        }
        requests.post(url, json=data)

    def post_submenus_batch(self, submenus: list, menu_id: str) -> None:
        """Запостить новые подменю в базу списком."""
        for submenu in submenus:
            self.post_submenu(
                submenu=submenu,
                menu_id=menu_id,
            )

    def post_dish(
        self,
        dish: dict[str, str],
        submenu_id: str,
        menu_id: str,
    ) -> None:
        """Запостить новое блюдо в базу."""
        url = PREFIX_LINK + DISHES_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        data = {
            'id': dish['id'],
            'title': dish['title'],
            'description': dish['description'],
            'price': dish['price'],
        }
        requests.post(url, json=data)

    def post_dishes_batch(
        self,
        dishes: list,
        submenu_id: str,
        menu_id: str,
    ) -> None:
        """Запостить новые блюда в базу списком."""
        for dish in dishes:
            self.post_dish(
                dish=dish,
                submenu_id=submenu_id,
                menu_id=menu_id,
            )

    def patch_menu(self, menu: dict[str, str | list]) -> None:
        """Обновить данные о меню в базе."""
        data = {
            'title': menu['title'],
            'description': menu['description'],
        }
        url = PREFIX_LINK + MENU_LINK.format(menu_id=menu['id'])
        requests.patch(url, json=data)

    def check_menu(self, menu: dict[str, str | list]) -> None:
        """Проверить состояние меню в базе и по необходимости обновить."""
        url = PREFIX_LINK + MENU_LINK.format(menu_id=menu['id'])
        current_menu = requests.get(url).json()
        if current_menu['title'] != menu['title'] or \
                current_menu['description'] != menu['description']:
            self.patch_menu(menu=menu)

    def patch_submenu(
        self,
        submenu: dict[str, str | list],
        menu_id: str,
    ) -> None:
        """Обновить данные о подменю в базе."""
        data = {
            'title': submenu['title'],
            'description': submenu['description'],
        }
        url = PREFIX_LINK + SUBMENU_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu['id'],
        )
        requests.patch(url, json=data)

    def check_submenu(
        self,
        submenu: dict[str, str | list],
        menu_id: str,
    ) -> None:
        """Проверить состояние подменю в базе и по необходимости обновить."""
        url = PREFIX_LINK + SUBMENU_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu['id'],
        )
        current_submenu = requests.get(url).json()
        if current_submenu['title'] != submenu['title'] or \
                current_submenu['description'] != submenu['description']:
            self.patch_submenu(submenu=submenu, menu_id=menu_id)

    def patch_dish(
        self,
        dish: dict[str, str],
        submenu_id: str,
        menu_id: str,
    ) -> None:
        """Обновить данные о блюде в базе."""
        data = {
            'title': dish['title'],
            'description': dish['description'],
            'price': dish['price'],
        }
        url = PREFIX_LINK + DISH_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish['id'],
        )
        requests.patch(url, json=data)

    def check_dish(
        self,
        dish: dict[str, str],
        submenu_id: str,
        menu_id: str,
    ) -> None:
        """Проверить состояние блюда в базе и по необходимости обновить."""
        url = PREFIX_LINK + DISH_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish['id'],
        )
        current_dish = requests.get(url).json()
        if current_dish['title'] != dish['title'] or \
                current_dish['description'] != dish['description'] or \
                current_dish['price'] != dish['price']:
            self.patch_dish(
                dish=dish,
                submenu_id=submenu_id,
                menu_id=menu_id,
            )

    def delete_menu(self, menu_id: str) -> None:
        """Удалить меню из базы."""
        url = PREFIX_LINK + MENU_LINK.format(menu_id=menu_id)
        requests.delete(url)

    def delete_submenu(self, submenu_id: str, menu_id: str) -> None:
        """Удалить подменю из базы."""
        url = PREFIX_LINK + SUBMENU_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        requests.delete(url)

    def delete_dish(self, dish_id: str, menu_id: str, submenu_id: str) -> None:
        """Удалить блюдо из базы."""
        url = PREFIX_LINK + DISH_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        requests.delete(url)

    def check_dishes(
        self,
        dishes: list[dict[str, str]],
        menu_id: str,
        submenu_id: str,
    ) -> None:
        """Проверить состояние блюд в базе и привести
        в соответствие с файлом."""
        dishes_id = self.get_dishes_from_db(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        for dish in dishes:
            if dish['id'] not in dishes_id:
                self.post_dish(
                    dish=dish,
                    submenu_id=submenu_id,
                    menu_id=menu_id,
                )
            else:
                self.check_dish(dish, submenu_id, menu_id)
                dishes_id.remove(dish['id'])
        for id in dishes_id:
            self.delete_dish(
                dish_id=id,
                menu_id=menu_id,
                submenu_id=submenu_id,
            )

    def check_submenus(
        self,
        submenus: list[dict],
        menu_id: str,
    ) -> None:
        """Проверить состояние подменю в базе и привести
        в соответствие с файлом."""
        submenus_id = self.get_submenus_from_db(menu_id)
        for submenu in submenus:
            if submenu['id'] not in submenus_id:
                self.post_submenu(
                    submenu=submenu,
                    menu_id=menu_id,
                )
                self.post_dishes_batch(
                    dishes=submenu['dishes'],
                    submenu_id=submenu['id'],
                    menu_id=menu_id,
                )
            else:
                self.check_submenu(
                    submenu=submenu,
                    menu_id=menu_id,
                )
                if submenu['dishes']:
                    self.check_dishes(
                        dishes=submenu['dishes'],
                        menu_id=menu_id,
                        submenu_id=submenu['id'],
                    )
                submenus_id.remove(submenu['id'])
        for id in submenus_id:
            self.delete_submenu(
                submenu_id=id,
                menu_id=menu_id,
            )

    def check_menus(self) -> None:
        """Проверить состояние меню в базе и привести
        в соответствие с файлом."""
        menus_id = self.get_menus_from_db()
        for menu in self.parser_data:
            if menu['id'] not in menus_id:
                self.post_menu(menu=menu)
                self.post_submenus_batch(
                    submenus=menu['submenus'],
                    menu_id=menu['id'],
                )
                for submenu in menu['submenus']:
                    self.post_dishes_batch(
                        dishes=submenu['dishes'],
                        submenu_id=submenu['id'],
                        menu_id=menu['id'],
                    )
            else:
                self.check_menu(menu=menu)
                if menu['submenus']:
                    self.check_submenus(
                        submenus=menu['submenus'],
                        menu_id=menu['id'],
                    )
                menus_id.remove(menu['id'])
        for id in menus_id:
            self.delete_menu(menu_id=id)

    def run(self) -> None:
        """Запустить обновление данных в базе."""
        self.check_menus()
