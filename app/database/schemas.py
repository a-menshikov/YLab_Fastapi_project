from pydantic import BaseModel


class MenuBase(BaseModel):
    """Базовая схема меню."""

    title: str
    description: str


class MenuPost(MenuBase):
    """Схема для создания нового меню."""

    pass


class MenuRead(MenuBase):
    """Схема для чтения меню."""

    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    """Базовая схема меню."""

    title: str
    description: str


class SubmenuPost(SubmenuBase):
    """Схема для создания нового меню."""

    pass


class SubmenuRead(SubmenuBase):
    """Схема для чтения меню."""

    id: str
    menu_id: str
    dishes_count: int

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    """Базовая схема блюда."""

    title: str
    description: str
    price: float


class DishPost(DishBase):
    """Схема для создания нового блюда."""

    pass


class DishRead(DishBase):
    """Схема для чтения блюда."""

    id: str
    submenu_id: str

    class Config:
        orm_mode = True
