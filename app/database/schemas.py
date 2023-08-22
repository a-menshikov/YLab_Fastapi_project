from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, validator


class MenuBase(BaseModel):
    """Базовая схема меню."""

    title: str
    description: str


class MenuPost(MenuBase):
    """Схема для создания нового меню."""

    id: str | None


class MenuWithID(MenuBase):
    """Базовая схема меню c id."""

    id: UUID

    @validator('id')
    def validate_id(cls, value: UUID) -> str:
        """Перевод id в строку для вывода"""
        return str(value)


class MenuRead(MenuWithID):
    """Схема для чтения меню."""

    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    """Базовая схема меню."""

    title: str
    description: str


class SubmenuWithID(SubmenuBase):
    """Базовая схема подменю c id."""

    id: UUID

    @validator('id')
    def validate_id(cls, value: UUID) -> str:
        """Перевод id в строку для вывода"""
        return str(value)


class SubmenuPost(SubmenuBase):
    """Схема для создания нового меню."""

    id: str | None


class SubmenuRead(SubmenuWithID):
    """Схема для чтения меню."""

    menu_id: UUID
    dishes_count: int

    class Config:
        orm_mode = True

    @validator('menu_id')
    def validate_submenu_id(cls, value: UUID) -> str:
        """Перевод submenu_id в строку для вывода"""
        return str(value)


class DishBase(BaseModel):
    """Базовая схема блюда."""

    title: str
    description: str


class DishWithID(DishBase):
    """Базовая схема Блюда c id."""

    id: UUID

    @validator('id')
    def validate_id(cls, value: UUID) -> str:
        """Перевод id в строку для вывода"""
        return str(value)


class DishPost(DishBase):
    """Схема для создания нового блюда."""

    id: str | None
    discount: int | None
    price: str

    @validator('price')
    def validate_price(cls, value: str) -> Decimal:
        """Округление входящей цены до 2 знаков."""
        return Decimal(value).quantize(Decimal('0.00'))

    @validator('discount')
    def validate_discount(cls, value: int) -> int:
        """Валидация скидки."""
        if value > 100 or value < 0:
            raise ValueError(
                'Скидка должна находиться в диапазоне от 0 до 100'
            )
        return value


class DishRead(DishWithID):
    """Схема для чтения блюда."""

    submenu_id: UUID
    discount: int
    price: Decimal

    class Config:
        extra = 'ignore'
        orm_mode = True

    @validator('price')
    def validate_price(cls, value: Decimal, values: dict) -> str:
        """Расчёт цены со скидкой и перевод в строку для вывода."""
        discount = values.get('discount')
        if discount:
            value = round(float(value) * (1 - discount / 100), 2)
        return str(value)

    @validator('submenu_id')
    def validate_submenu_id(cls, value: UUID) -> str:
        """Перевод submenu_id в строку для вывода"""
        return str(value)


class DishReadFullGet(DishWithID):
    """Схема для чтения блюда при полной выдаче базы."""

    discount: int
    price: Decimal

    class Config:
        extra = 'ignore'
        orm_mode = True

    @validator('price')
    def validate_price(cls, value: Decimal, values: dict) -> str:
        """Расчёт цены со скидкой и перевод в строку для вывода."""
        discount = values.get('discount')
        if discount:
            value = round(float(value) * (1 - discount / 100), 2)
        return str(value)


class SubmenuReadFullGet(SubmenuWithID):
    """Схема для чтения подменю при полной выдаче базы."""

    dishes: list[DishReadFullGet]

    class Config:
        extra = 'ignore'
        orm_mode = True


class MenuReadFullGet(MenuWithID):
    """Схема для чтения меню при полной выдаче базы."""

    submenus: list[SubmenuReadFullGet]

    class Config:
        extra = 'ignore'
        orm_mode = True
