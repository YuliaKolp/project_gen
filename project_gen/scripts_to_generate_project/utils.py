import os
import subprocess
import sys
import traceback
from pathlib import Path

from cookiecutter.main import cookiecutter


def run_command(command: list[str]) -> str:
    print(" ".join(command))
    result = subprocess.run(args=command, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}, for command: {' '.join(command)}")
        sys.exit(1)
    return result.stdout.strip()


def check_git_repository() -> None:
    command = ["git", "rev-parse", "--is-inside-work-tree"]
    is_work_tree = run_command(command)
    if not is_work_tree:
        print("Not a git repository")
        sys.exit(1)


def get_git_repository_info() -> str:
    remote_url = run_command(["git", "config", "--get", "remote.origin.url"])
    remote = remote_url.split("/")[-1].split(".git")[0]
    return remote


def get_git_user_info() -> tuple[str, str]:
    user_email = run_command(["git", "config", "--get", "user.email"])
    user_name = run_command(["git", "config", "--get", "user.name"])
    email_value = user_email if user_email else "user_name@example.com"
    name_value = user_name if user_name else "user_name"
    return email_value, name_value


def create_project(template: str) -> None:
    template = template or str(Path(__file__).parent.parent / "templates" / "project")
    print("Creating project")
    check_git_repository()
    user_email, user_name = get_git_user_info()
    authors = f"{user_name} <{user_email}>"

    remote = get_git_repository_info()

    venv_dir = os.environ.get("VIRTUAL_ENV")
    root_project_dir = os.path.dirname(venv_dir)
    output_dir = os.path.join(root_project_dir, "output_dir")

    extra_context = {
        "user_email": user_email,
        "authors": authors,
        "project_name": remote,
        "repository": remote,
        "description": "project_gen project",
        "project_slug": "project-gen",
        "version": "0.1.0",
    }

    try:
        cookiecutter(
            template=template,
            no_input=True,
            overwrite_if_exists=True,
            output_dir=output_dir,
            extra_context=extra_context,
        )
    except Exception as e:
        print(f"Предупреждение: возникла ошибка в хуке, но она проигнорирована: {e}")
        traceback.print_exc()
    finally:
        sys.exit(0)


def setup(template: str | None = None) -> None:
    check_git_repository()
    create_project(template)
