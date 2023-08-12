from fastapi import FastAPI

from app.api.dishes.api import dish_router
from app.api.menus.api import menu_router
from app.api.submenus.api import submenu_router
from app.database.db_loader import init_db
from app.tasks.tasks import task_test

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
    await init_db()
    task_test.delay()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
