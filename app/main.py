from app.database.db_loader import Base, engine
from app.database.models import Menu
from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/api/v1/menus")
def menus():
    return []
