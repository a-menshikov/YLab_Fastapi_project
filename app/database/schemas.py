from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, validator


class MenuBase(BaseModel):
    """Базовая схема меню."""

    title: str
    description: str


class MenuPost(MenuBase):
    """Схема для создания нового меню."""

    pass


class MenuRead(MenuBase):
    """Схема для чтения меню."""

    id: UUID
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True

    @validator('id')
    def validate_id(cls, value):
        return str(value)


class SubmenuBase(BaseModel):
    """Базовая схема меню."""

    title: str
    description: str


class SubmenuPost(SubmenuBase):
    """Схема для создания нового меню."""

    pass


class SubmenuRead(SubmenuBase):
    """Схема для чтения меню."""

    id: UUID
    menu_id: UUID
    dishes_count: int

    class Config:
        orm_mode = True

    @validator('id')
    def validate_id(cls, value):
        return str(value)

    @validator('menu_id')
    def validate_submenu_id(cls, value):
        return str(value)


class DishBase(BaseModel):
    """Базовая схема блюда."""

    title: str
    description: str
    price: str


class DishPost(DishBase):
    """Схема для создания нового блюда."""

    @validator('price')
    def validate_price(cls, value):
        """Округление цены до 2 знаков."""
        return Decimal(value).quantize(Decimal('0.00'))


class DishRead(DishBase):
    """Схема для чтения блюда."""

    id: UUID
    submenu_id: UUID
    price: Decimal

    class Config:
        orm_mode = True

    @validator('price')
    def validate_price(cls, value):
        return str(value)

    @validator('id')
    def validate_id(cls, value):
        return str(value)

    @validator('submenu_id')
    def validate_submenu_id(cls, value):
        return str(value)
