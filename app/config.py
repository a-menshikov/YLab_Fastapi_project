import os

from dotenv import load_dotenv

load_dotenv()

PREFIX_LINK = 'http://backend:80/api/v1'
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
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_DEFAULT_PORT = os.getenv('RABBITMQ_DEFAULT_PORT')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')

EXPIRATION = 3600

MENU_FILE_PATH = '/code/app/admin/Menu.xlsx'

conn_url = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
            f'@database/{POSTGRES_DB}')
