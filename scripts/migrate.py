import os
import argparse
from utils import run_process

alembic_env_file = "./migrations/env.py"
end_marker = "### replace before\n"
start_marker = "### replace after\n"


def main():
    parser = argparse.ArgumentParser(
        prog="migration", description="CLI tool used for alembic migrations"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run", help="Runs migrations")

    gen_parser = subparsers.add_parser("gen", help="Generates migrations")
    gen_parser.add_argument("-m", "--message", required=True, help="migration name")

    args = parser.parse_args()

    if args.command == "gen":
        import_modules()
        generate_migrations(args.message)
    if args.command == "run":
        run_migrations()


def generate_migrations(message: str):
    run_process(["alembic", "revision", "--autogenerate", "-m", message])


def run_migrations():
    run_process(["alembic", "upgrade", "head"])


def import_modules():
    # 1. discover models
    model_imports = []
    for root, _, files in os.walk("."):
        if any(x in root for x in ["venv", "__pycache__", "migrations"]):
            continue
        for file in files:
            if file == "models.py":
                module = (
                    os.path.relpath(os.path.join(root, file), ".")
                    .replace(os.path.sep, ".")
                    .removesuffix(".py")
                )
                model_imports.append(f"from {module} import *")

    # 2. update file
    try:
        with open(alembic_env_file, "r") as f:
            lines = f.readlines()

        start_idx = lines.index(start_marker)
        end_idx = lines.index(end_marker)

        while end_idx - start_idx > 1:
            end_idx -= 1
            lines.pop(end_idx)

        # reconstruct:
        # [start marker] + [new content] + [end marker]
        new_content = "\n".join(model_imports) + "\n"
        lines.insert(end_idx, new_content)

        with open(alembic_env_file, "w") as f:
            f.writelines(lines)

        print("Successfully updated env.py without duplicating markers.")

    except ValueError:
        print("Markers not found. Ensure both exist exactly as defined.")


if __name__ == "__main__":
    main()
