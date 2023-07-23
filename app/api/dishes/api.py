from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# from app.api.dishes.crud import
# from app.api.menus.crud import get_menu_by_id
from app.api.submenus.crud import get_submenu_by_id
from app.database.db_loader import get_db
from app.database.schemas import DishRead, DishPost


dish_router = APIRouter(prefix="/api/v1/menus")


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes",
                 response_model=DishRead)
def get_dishes(menu_id: str, submenu_id: str,
               db: Session = Depends(get_db)):
    """Получение всех блюд конкретного подменю."""
    current_submenu = get_submenu_by_id(db=db, id=submenu_id)
    # проверки на существование всего
    dishes = current_submenu.dishes
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(dishes),
    )


@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes",
                  response_model=DishRead)
def post_new_dish(menu_id: str, submenu_id: str, dish: DishPost,
                  db: Session = Depends(get_db)):
    """Добавление нового блюда."""
    pass


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                 response_model=DishRead)
def get_dish(menu_id: str, submenu_id: str, dish_id: str,
             db: Session = Depends(get_db)):
    """Получение блюда по id."""
    pass


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                   response_model=DishRead)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str,
               updated_dish: DishPost, db: Session = Depends(get_db)):
    """Изменение блюда по id."""
    pass


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str,
                db: Session = Depends(get_db)):
    """Удаление блюда по id."""
    pass
