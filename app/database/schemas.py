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

    class Config:
        orm_mode = True
