from fastapi import APIRouter
from sqlmodel import select

from .models import ExampleModel
from ...dependencies import SessionDep

router = APIRouter(
    prefix="/example",
    tags=["example"],
)


@router.get("/models")
async def greet(session: SessionDep) -> list[ExampleModel]:
    models = session.exec(select(ExampleModel)).all()
    return list(models)


@router.post("/models")
async def createExampleModel(model: ExampleModel, session: SessionDep):
    session.add(model)
    session.commit()
    session.refresh(model)
    return model
