from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuPost(MenuBase):
    pass


class MenuRead(MenuBase):
    id: str

    class Config:
        orm_mode = True
