from fastapi import FastAPI

from app.api.dishes.api import dish_router
from app.api.menus.api import menu_router
from app.api.submenus.api import submenu_router
from app.database.db_loader import Base, engine
from app.database.models import Dish, Menu, Submenu

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
