from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.service_repository import MenuService
from app.config import MENU_LINK, MENUS_LINK
from app.database.schemas import MenuPost, MenuRead, MenuReadFullGet

menu_router = APIRouter(prefix='/api/v1')


@menu_router.get(
    MENUS_LINK,
    response_model=list[MenuRead],
    status_code=200,
    tags=['Меню'],
    summary='Все меню',
)
async def get_menus(
    background_tasks: BackgroundTasks,
    repo: MenuService = Depends()
) -> list[MenuRead]:
    """Получение всех меню."""
    return await repo.get_all_menus(background_tasks=background_tasks)


@menu_router.post(
    MENUS_LINK, response_model=MenuRead,
    status_code=201,
    tags=['Меню'],
    summary='Добавить меню',
)
async def post_new_menu(
    background_tasks: BackgroundTasks,
    menu: MenuPost,
    repo: MenuService = Depends()
) -> MenuRead:
    """Добавление нового меню."""
    try:
        return await repo.create_menu(menu=menu,
                                      background_tasks=background_tasks)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@menu_router.get(
    MENU_LINK,
    response_model=MenuRead,
    status_code=200,
    tags=['Меню'],
    summary='Получить меню',
)
async def get_menu(
    background_tasks: BackgroundTasks,
    menu_id: str,
    repo: MenuService = Depends(),
) -> MenuRead:
    """Получение меню по id."""
    try:
        return await repo.get_menu_by_id(id=menu_id,
                                         background_tasks=background_tasks)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@menu_router.patch(
    MENU_LINK,
    response_model=MenuRead,
    status_code=200,
    tags=['Меню'],
    summary='Изменить меню',
)
async def patch_menu(
    background_tasks: BackgroundTasks,
    menu_id: str,
    updated_menu: MenuPost,
    repo: MenuService = Depends(),
) -> MenuRead:
    """Изменение меню по id."""
    try:
        return await repo.update_menu(
            menu_id=menu_id,
            updated_menu=updated_menu,
            background_tasks=background_tasks,
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


@menu_router.delete(
    '/menus/{menu_id}',
    status_code=200,
    tags=['Меню'],
    summary='Удалить меню',
)
async def destroy_menu(menu_id: str,
                       background_tasks: BackgroundTasks,
                       repo: MenuService = Depends(),) -> JSONResponse:
    """Удаление меню по id."""
    try:
        await repo.delete_menu(menu_id=menu_id,
                               background_tasks=background_tasks)
        return JSONResponse(
            status_code=200,
            content='menu deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@menu_router.get(
    '/fullbase',
    status_code=200,
    response_model=list[MenuReadFullGet],
    tags=['Меню'],
    summary='Развернутая структура всей базы меню со связанными объектами',
)
async def get_full_base_menu(
    background_tasks: BackgroundTasks,
    repo: MenuService = Depends()
) -> list[MenuReadFullGet]:
    """Получение всех меню c развернутым списком блюд и подменю."""
    return await repo.get_full_base_menu(background_tasks=background_tasks)
