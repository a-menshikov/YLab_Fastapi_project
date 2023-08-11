import os

from dotenv import load_dotenv

load_dotenv()

MENUS_LINK = '/menus'
MENU_LINK = '/menus/{menu_id}'
SUBMENUS_LINK = '/menus/{menu_id}/submenus'
SUBMENU_LINK = '/menus/{menu_id}/submenus/{submenu_id}'
DISHES_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes'
DISH_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
EXPIRATION = 3600
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
conn_url = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
            f'@database/{POSTGRES_DB}')
