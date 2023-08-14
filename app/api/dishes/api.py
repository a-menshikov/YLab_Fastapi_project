from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.dishes.service_repository import DishService
from app.config import DISH_LINK, DISHES_LINK
from app.database.schemas import DishPost, DishRead

dish_router = APIRouter(prefix='/api/v1')


@dish_router.get(
    DISHES_LINK,
    response_model=list[DishRead],
    status_code=200,
    tags=['Блюда'],
    summary='Все блюда подменю',
)
async def get_dishes(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    repo: DishService = Depends(),
) -> list[DishRead]:
    """Получение всех блюд конкретного подменю."""
    return await repo.get_all_dishes(
        submenu_id=submenu_id,
        menu_id=menu_id,
        background_tasks=background_tasks,
    )


@dish_router.post(
    DISHES_LINK,
    response_model=DishRead,
    status_code=201,
    tags=['Блюда'],
    summary='Добавить блюдо',
)
async def post_new_dish(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish: DishPost,
    repo: DishService = Depends(),
) -> DishRead:
    """Добавление нового блюда."""
    try:
        return await repo.create_dish(
            dish=dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            background_tasks=background_tasks,
        )
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


@dish_router.get(
    DISH_LINK,
    response_model=DishRead,
    status_code=200,
    tags=['Блюда'],
    summary='Получить блюдо',
)
async def get_dish(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    repo: DishService = Depends(),
) -> DishRead:
    """Получение блюда по id."""
    try:
        return await repo.get_dish_by_id(
            id=dish_id,
            menu_id=menu_id,
            submenu_id=submenu_id,
            background_tasks=background_tasks,
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@dish_router.patch(
    DISH_LINK,
    response_model=DishRead,
    status_code=200,
    tags=['Блюда'],
    summary='Изменить блюдо',
)
async def patch_dish(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    updated_dish: DishPost,
    repo: DishService = Depends(),
) -> DishRead:
    """Изменение блюда по id."""
    try:
        return await repo.update_dish(
            dish_id=dish_id,
            submenu_id=submenu_id,
            menu_id=menu_id,
            updated_dish=updated_dish,
            background_tasks=background_tasks,
        )
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


@dish_router.delete(
    DISH_LINK,
    status_code=200,
    tags=['Блюда'],
    summary='Удалить блюдо',
)
async def destroy_dish(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    repo: DishService = Depends(),
) -> JSONResponse:
    """Удаление блюда по id."""
    try:
        await repo.delete_dish(
            dish_id=dish_id,
            menu_id=menu_id,
            background_tasks=background_tasks,
        )
        return JSONResponse(
            status_code=200,
            content='dish deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
