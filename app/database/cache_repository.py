import pickle

from fastapi import Depends

from app.api.dishes.crud_repository import DishRepository
from app.api.menus.crud_repository import MenuRepository
from app.api.submenus.crud_repository import SubmenuRepository
from app.database.db_loader import EXPIRATION, redis


class СacheRepository():
    def __init__(self, menu_repo: MenuRepository = Depends(),
                 submenu_repo: SubmenuRepository = Depends(),
                 dish_repo: DishRepository = Depends()) -> None:
        self.cacher = redis
        self.menu_repo = menu_repo
        self.submenu_repo = submenu_repo
        self.dish_repo = dish_repo

    def set_all_dishes_cache(self, submenu_id, items):
        redis.set(f'all_dishes_{submenu_id}',
                  pickle.dumps(items), ex=EXPIRATION)

    def get_all_dishes_cache(self, submenu_id):
        cache = redis.get(f'all_dishes_{submenu_id}')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    def set_dish_cache(self, item):
        redis.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def get_dish_cache(self, id):
        cache = redis.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def delete_related_dish_cache(self, submenu_id, menu_id):
        self.delete_all_dish_cache(submenu_id)
        redis.delete(submenu_id)
        self.delete_all_submenu_cache(menu_id)
        redis.delete(menu_id)
        self.delete_all_menu_cache()

    def create_dish_cache(self, item, submenu_id, menu_id):
        self.delete_related_dish_cache(submenu_id, menu_id)
        self.set_dish_cache(item)

    def update_dish_cache(self, item):
        self.delete_all_dish_cache(str(item.submenu_id))
        self.set_dish_cache(item)

    def delete_dish_cache(self, dish_id, submenu_id, menu_id):
        redis.delete(dish_id)
        self.delete_related_dish_cache(submenu_id, menu_id)

    def delete_all_dish_cache(self, submenu_id):
        redis.delete(f'all_dishes_{submenu_id}')

    def set_all_submenus_cache(self, menu_id, items):
        redis.set(f'all_submenus_{menu_id}',
                  pickle.dumps(items), ex=EXPIRATION)

    def get_all_submenus_cache(self, menu_id):
        cache = redis.get(f'all_submenus_{menu_id}')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    def set_submenu_cache(self, item):
        redis.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def get_submenu_cache(self, id):
        cache = redis.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def create_submenu_cache(self, item):
        self.delete_menu_cache(str(item.menu_id))
        self.delete_all_menu_cache()
        self.delete_all_submenu_cache(str(item.menu_id))
        self.set_submenu_cache(item)

    def update_submenu_cache(self, item):
        self.delete_all_submenu_cache(str(item.menu_id))
        self.set_submenu_cache(item)

    def delete_submenu_cache(self, submenu_id, menu_id):
        redis.delete(submenu_id)
        self.delete_all_dish_cache(submenu_id)
        self.delete_all_submenu_cache(menu_id)
        dishes = self.dish_repo.get_all_dishes(submenu_id)
        if dishes:
            for dish in dishes:
                self.delete_dish_cache(str(dish.id), submenu_id, menu_id)

    def delete_all_submenu_cache(self, menu_id):
        redis.delete(f'all_submenus_{menu_id}')

    def set_all_menus_cache(self, items):
        redis.set('all_menus', pickle.dumps(items), ex=EXPIRATION)

    def get_all_menus_cache(self):
        cache = redis.get('all_menus')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    def set_menu_cache(self, item):
        redis.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def get_menu_cache(self, id):
        cache = redis.get(id)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def create_update_menu_cache(self, item):
        self.delete_all_menu_cache()
        redis.set(str(item.id), pickle.dumps(item), ex=EXPIRATION)

    def delete_all_menu_cache(self):
        redis.delete('all_menus')

    def delete_menu_cache(self, menu_id):
        redis.delete(menu_id)
        self.delete_all_menu_cache()
        self.delete_all_submenu_cache(menu_id)
        submenus = self.submenu_repo.get_all_submenus(menu_id)
        if submenus:
            for submenu in submenus:
                self.delete_submenu_cache(str(submenu.id), menu_id)
