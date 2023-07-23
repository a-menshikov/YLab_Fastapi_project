from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.dishes.crud import create_dish, get_dish_by_id, update_dish
from app.api.submenus.crud import get_submenu_by_id
from app.database.db_loader import get_db
from app.database.schemas import DishRead, DishPost
from app.database.services import check_objects


dish_router = APIRouter(prefix="/api/v1/menus")


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes",
                 response_model=List[DishRead])
def get_dishes(menu_id: str, submenu_id: str,
               db: Session = Depends(get_db)):
    """Получение всех блюд конкретного подменю."""
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_submenu = get_submenu_by_id(db=db, id=submenu_id)
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
    try:
        check_objects(db=db, menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    new_dish = create_dish(db=db, dish=dish, submenu_id=submenu_id)
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(new_dish),
    )


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                 response_model=DishRead)
def get_dish(menu_id: str, submenu_id: str, dish_id: str,
             db: Session = Depends(get_db)):
    """Получение блюда по id."""
    try:
        check_objects(db=db, menu_id=menu_id,
                      submenu_id=submenu_id, dish_id=dish_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_dish = get_dish_by_id(db=db, id=dish_id)
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(current_dish),
    )


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                   response_model=DishRead)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str,
               updated_dish: DishPost, db: Session = Depends(get_db)):
    """Изменение блюда по id."""
    try:
        check_objects(db=db, menu_id=menu_id,
                      submenu_id=submenu_id, dish_id=dish_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_dish = get_dish_by_id(db=db, id=dish_id)
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(update_dish(
            db,
            current_dish,
            updated_dish,
        ))
    )


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str,
                db: Session = Depends(get_db)):
    """Удаление блюда по id."""
    try:
        check_objects(db=db, menu_id=menu_id,
                      submenu_id=submenu_id, dish_id=dish_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    current_dish = get_dish_by_id(db=db, id=dish_id)
    db.delete(current_dish)
    db.commit()
    return JSONResponse(
        status_code=200,
        content='dish deleted',
    )
