import os
import argparse
from utils import run_process


models_template = """"
from sqlmodel import Field, SQLModel


class ExampleModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
"""

routes_template = """
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
"""


def main():
    parser = argparse.ArgumentParser(
        prog="Application Utility", description="Tool used to create new stacks"
    )

    parser.add_argument("app_name", help="name of the new application")

    args = parser.parse_args()
    name = args.app_name
    create_new_stack(name)


def create_new_stack(stack_name: str):
    path = "./apps/" + stack_name + "/"
    run_process(["touch", path + "__init__.py"])

    run_process(["touch", path + "models.py"])
    run_process(["echo", f'"{models_template}"', ">", path + "models.py"])

    run_process(["touch", path + "routes.py"])
    run_process(["echo", f'"{routes_template}"', ">", path + "routes.py"])


if __name__ == "__main__":
    main()
