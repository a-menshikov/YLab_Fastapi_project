from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.submenus.service_repository import SubmenuService
from app.config import SUBMENU_LINK, SUBMENUS_LINK
from app.database.schemas import SubmenuPost, SubmenuRead

submenu_router = APIRouter(prefix='/api/v1')


@submenu_router.get(
    SUBMENUS_LINK,
    response_model=list[SubmenuRead],
    status_code=200,
    tags=['Подменю'],
    summary='Все подменю',
)
async def get_submenus(
    background_tasks: BackgroundTasks,
    menu_id: str,
    repo: SubmenuService = Depends(),
) -> list[SubmenuRead]:
    """Получение всех подменю конкретного меню."""
    return await repo.get_all_submenus(
        menu_id=menu_id,
        background_tasks=background_tasks,
    )


@submenu_router.post(
    SUBMENUS_LINK,
    response_model=SubmenuRead,
    status_code=201,
    tags=['Подменю'],
    summary='Добавить подменю',
)
async def post_new_submenu(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu: SubmenuPost,
    repo: SubmenuService = Depends(),
) -> SubmenuRead:
    """Добавление нового подменю к конкретному меню."""
    try:
        return await repo.create_submenu(
            submenu=submenu,
            menu_id=menu_id,
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


@submenu_router.get(
    SUBMENU_LINK,
    response_model=SubmenuRead,
    status_code=200,
    tags=['Подменю'],
    summary='Получить подменю',
)
async def get_submenu(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    repo: SubmenuService = Depends(),
) -> SubmenuRead:
    """Получение подменю конкретного меню по id."""
    try:
        return await repo.get_submenu_by_id(
            id=submenu_id,
            menu_id=menu_id,
            background_tasks=background_tasks,
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@submenu_router.patch(
    SUBMENU_LINK,
    response_model=SubmenuRead,
    status_code=200,
    tags=['Подменю'],
    summary='Изменить подменю',
)
async def patch_submenu(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    updated_submenu: SubmenuPost,
    repo: SubmenuService = Depends(),
) -> SubmenuRead:
    """Обновление подменю конкретного меню по id."""
    try:
        return await repo.update_submenu(
            submenu_id=submenu_id,
            updated_submenu=updated_submenu,
            background_tasks=background_tasks
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@submenu_router.delete(
    SUBMENU_LINK,
    status_code=200,
    tags=['Подменю'],
    summary='Удалить подменю',
)
async def destroy_submenu(
    background_tasks: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    repo: SubmenuService = Depends(),
) -> JSONResponse:
    """Удаление подменю конкретного меню по id."""
    try:
        await repo.delete_submenu(
            menu_id=menu_id,
            submenu_id=submenu_id,
            background_tasks=background_tasks,
        )
        return JSONResponse(
            status_code=200,
            content='submenu deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
