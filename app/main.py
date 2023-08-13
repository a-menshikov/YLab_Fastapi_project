from fastapi import FastAPI

from app.api.dishes.api import dish_router
from app.api.menus.api import menu_router
from app.api.submenus.api import submenu_router
from app.database.db_loader import init_db
from app.tasks.tasks import update_base

app = FastAPI(
    title='Restaurant API',
    description='Приложение для управления меню ресторана',
    version='4.0.0',
    openapi_tags=[
        {
            'name': 'Меню',
            'description': 'Операции с меню',
        },
        {
            'name': 'Подменю',
            'description': 'Операции с подменю',
        },
        {
            'name': 'Блюда',
            'description': 'Операции с блюдами',
        },
    ]
)


@app.on_event('startup')
async def on_startup():
    """Выполняется при запуске приложения.
    Инициализирует БД и запускает задачу обновления БД."""
    await init_db()
    update_base.delay()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
