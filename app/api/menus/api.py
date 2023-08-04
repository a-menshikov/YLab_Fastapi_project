from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import FlushError, NoResultFound

from app.api.menus.repositories import MenuService
from app.database.schemas import MenuPost, MenuRead

menu_router = APIRouter(prefix='/api/v1')


@menu_router.get('/menus', response_model=list[MenuRead])
def get_menus(repo: MenuService = Depends()):
    """Получение всех меню."""
    return repo.get_all_menus()


@menu_router.post('/menus', response_model=MenuRead, status_code=201)
def post_new_menu(menu: MenuPost, repo: MenuService = Depends()):
    """Добавление нового меню."""
    try:
        return repo.create_menu(menu=menu)
    except FlushError as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@menu_router.get('/menus/{menu_id}', response_model=MenuRead)
def get_menu(menu_id: str, repo: MenuService = Depends()):
    """Получение меню по id."""
    try:
        return repo.get_menu_by_id(id=menu_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )


@menu_router.patch('/menus/{menu_id}', response_model=MenuRead)
def patch_menu(menu_id: str, updated_menu: MenuPost,
               repo: MenuService = Depends()):
    """Изменение меню по id."""
    try:
        return repo.update_menu(menu_id, updated_menu)
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


@menu_router.delete('/menus/{menu_id}')
def destroy_menu(menu_id: str, repo: MenuService = Depends()):
    """Удаление меню по id."""
    try:
        repo.delete_menu(menu_id=menu_id)
        return JSONResponse(
            status_code=200,
            content='menu deleted',
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=404,
            detail=error.args[0],
        )
