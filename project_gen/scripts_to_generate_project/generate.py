import os
import pathlib

import toml

from project_gen.scripts_to_generate_project.download import init
from project_gen.scripts_to_generate_project.handle_dirs import (
    move_directory_contents,
    safe_remove_dir,
)
from project_gen.scripts_to_generate_project.utils import run_command


def generate_api(
        package_name: str,
        swagger_url: str,
        openapi_generator_jar: str,
        templates: str | None = None
        ) -> None:
    templates = templates or str(pathlib.Path(__file__).parent.parent / "templates" / "python")
    command = ["java", "-jar", openapi_generator_jar,
               "generate", "-i", swagger_url,
               "-g", "python",
               "-o", package_name,
               "--library", "asyncio",
               "--package-name", package_name,
               "--skip-validate-spec",
               ]
    if templates:
        command.extend(["-t", templates])
    run_command(command)


def generate(templates: str | None = None) -> None:
    templates = templates or str(pathlib.Path(__file__).parent.parent / "templates" / "python")
    testproject_toml = os.path.join(str(pathlib.Path(__file__).parent.parent / "templates" / "project"), 'testproject.toml')

    venv_path = os.environ.get('VIRTUAL_ENV')
    project_root = os.path.dirname(venv_path)

    with open(testproject_toml) as config_file:
        config = toml.load(config_file)

    for http_service in config["http"]:
        package_name = http_service["service_name"].replace('-', '_')
        swagger_url = http_service["swagger"]

        openapi_generator_jar = init()
        generate_api(package_name=package_name, swagger_url=swagger_url, openapi_generator_jar=openapi_generator_jar, templates=templates)
        dst_folder = os.path.join(project_root, "clients", "http", package_name)
        move_directory_contents(f"{package_name}/{package_name}", dst_folder)
        safe_remove_dir(package_name)

