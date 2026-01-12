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
    models = (await session.execute(select(ExampleModel))).scalars().all()
    return list(models)


@router.post("/models")
async def createExampleModel(model: ExampleModel, session: SessionDep):
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


@router.put("/models")
async def create_model(model: ExampleModel, session: SessionDep):
    db_model = await session.merge(model)
    await session.commit()
    await session.refresh(db_model)
    return db_model
