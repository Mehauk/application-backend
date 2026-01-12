import argparse
from pathlib import Path

# Templates (Note: using f-strings if you want to inject the stack_name into the templates)
MODELS_TEMPLATE = """from sqlmodel import Field, SQLModel


class {Name}Model(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
"""

ROUTES_TEMPLATE = """from fastapi import APIRouter
from sqlmodel import select
from .models import {Name}Model
from ...dependencies import SessionDep

router = APIRouter(
    prefix="/{name}",
    tags=["{name}"],
)


@router.get("/models")
async def get_models(session: SessionDep) -> list[{Name}Model]:
    models = (await session.execute(select({Name}Model))).scalars().all()
    return list(models)


@router.post("/models")
async def create_model(model: {Name}Model, session: SessionDep):
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


@router.put("/models")
async def create_model(model: {Name}Model, session: SessionDep):
    db_model = await session.merge(model)
    await session.commit()
    await session.refresh(db_model)
    return db_model
"""

IMPORT_TEMPLATE = """from .apps.{name} import routes as {name}"""
ROUTE_ADD_TEMPLATE = """app.include_router({name}.router)"""


def create_new_stack(stack_name: str):
    main = Path("./main.py")
    # Use Pathlib for more robust path handling
    base_path = Path(f"./apps/{stack_name}")

    # 1. Create the directory (and parent /apps/ if missing)
    base_path.mkdir(parents=True, exist_ok=False)
    print(f"Creating stack in: {base_path.resolve()}")

    # 2. Define files to create
    files = {
        "__init__.py": "",
        "models.py": MODELS_TEMPLATE.replace("{name}", stack_name).replace(
            "{Name}", stack_name.capitalize()
        ),
        "routes.py": ROUTES_TEMPLATE.replace("{name}", stack_name).replace(
            "{Name}", stack_name.capitalize()
        ),
    }

    # 3. Write files using native Python (more reliable than shell echo)
    for filename, content in files.items():
        file_path = base_path / filename
        with open(file_path, "w") as f:
            f.write(content.strip())
        print(f"  + Created {filename}")

    with open(main, "r") as m:
        lines = m.readlines()

    with open(main, "w") as m2:
        import_end = "### import routes end\n"
        route_add_end = "### routers end\n"

        iid = lines.index(import_end)
        lines.insert(iid, IMPORT_TEMPLATE.replace("{name}", stack_name) + "\n")

        rid = lines.index(route_add_end)
        lines.insert(rid, ROUTE_ADD_TEMPLATE.replace("{name}", stack_name) + "\n")

        m2.writelines(lines)


def main():
    parser = argparse.ArgumentParser(
        prog="Application Utility", description="Tool used to create new stacks"
    )
    parser.add_argument("app_name", help="name of the new application")
    args = parser.parse_args()

    create_new_stack(args.app_name)
    print(f"\nSuccessfully created stack '{args.app_name}'")


if __name__ == "__main__":
    main()
