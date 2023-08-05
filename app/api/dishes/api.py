from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.dishes.service_repository import DishService
from app.database.schemas import DishPost, DishRead

dish_router = APIRouter(prefix='/api/v1/menus')


@dish_router.get('/{menu_id}/submenus/{submenu_id}/dishes',
                 response_model=list[DishRead])
def get_dishes(menu_id: str, submenu_id: str,
               repo: DishService = Depends()) -> list[DishRead]:
    """Получение всех блюд конкретного подменю."""
    return repo.get_all_dishes(submenu_id=submenu_id)


@dish_router.post('/{menu_id}/submenus/{submenu_id}/dishes',
                  response_model=DishRead, status_code=201)
def post_new_dish(menu_id: str, submenu_id: str, dish: DishPost,
                  repo: DishService = Depends()) -> DishRead:
    """Добавление нового блюда."""
    try:
        return repo.create_dish(dish=dish, menu_id=menu_id,
                                submenu_id=submenu_id)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@dish_router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                 response_model=DishRead)
def get_dish(menu_id: str, submenu_id: str, dish_id: str,
             repo: DishService = Depends()) -> DishRead:
    """Получение блюда по id."""
    try:
        return repo.get_dish_by_id(id=dish_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@dish_router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                   response_model=DishRead)
def patch_dish(menu_id: str, submenu_id: str, dish_id: str,
               updated_dish: DishPost, repo: DishService = Depends()
               ) -> DishRead:
    """Изменение блюда по id."""
    try:
        return repo.update_dish(dish_id, updated_dish)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@dish_router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def destroy_dish(menu_id: str, submenu_id: str, dish_id: str,
                 repo: DishService = Depends()) -> JSONResponse:
    """Удаление блюда по id."""
    try:
        repo.delete_dish(dish_id=dish_id, submenu_id=submenu_id,
                         menu_id=menu_id)
        return JSONResponse(
            status_code=200,
            content='dish deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
