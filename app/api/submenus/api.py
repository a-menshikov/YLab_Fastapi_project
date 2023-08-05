from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.submenus.service_repository import SubmenuService
from app.database.schemas import SubmenuPost, SubmenuRead

submenu_router = APIRouter(prefix='/api/v1/menus')


@submenu_router.get('/{menu_id}/submenus', response_model=list[SubmenuRead])
def get_submenus(menu_id: str, repo: SubmenuService = Depends()):
    """Получение всех подменю конкретного меню."""
    return repo.get_all_submenus(menu_id=menu_id)


@submenu_router.post('/{menu_id}/submenus', response_model=SubmenuRead,
                     status_code=201)
def post_new_submenu(menu_id: str, submenu: SubmenuPost,
                     repo: SubmenuService = Depends()):
    """Добавление нового подменю к конкретному меню."""
    try:
        return repo.create_submenu(submenu=submenu, menu_id=menu_id)
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


@submenu_router.get('/{menu_id}/submenus/{submenu_id}',
                    response_model=SubmenuRead)
def get_submenu(menu_id: str, submenu_id: str,
                repo: SubmenuService = Depends()):
    """Получение подменю конкретного меню по id."""
    try:
        return repo.get_submenu_by_id(id=submenu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@submenu_router.patch('/{menu_id}/submenus/{submenu_id}',
                      response_model=SubmenuRead)
def patch_submenu(menu_id: str, submenu_id: str, updated_submenu: SubmenuPost,
                  repo: SubmenuService = Depends()):
    """Обновление подменю конкретного меню по id."""
    try:
        return repo.update_submenu(submenu_id, updated_submenu)
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


@submenu_router.delete('/{menu_id}/submenus/{submenu_id}')
def destroy_submenu(menu_id: str, submenu_id: str,
                    repo: SubmenuService = Depends()):
    """Удаление подменю конкретного меню по id."""
    try:
        repo.delete_submenu(menu_id, submenu_id)
        return JSONResponse(
            status_code=200,
            content='submenu deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
