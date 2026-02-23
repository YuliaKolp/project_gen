import os
import pathlib

from project_gen.scripts_to_generate_project.download import download
from project_gen.scripts_to_generate_project.handle_dirs import (
    move_directory_contents,
    get_bin_dir,
    safe_remove_dir,
)
from project_gen.scripts_to_generate_project.utils import run_command


def genearte_api(
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


swagger_url = "http://185.185.143.231:8085/register/openapi.json"
templates = "C:\\Users\\skolp\\PycharmProjects\\openapi-generator\\modules\\openapi-generator\\src\\main\\resources\\python"
openapi_url = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.16.0/openapi-generator-cli-7.16.0.jar"

## get openapi_generator_jar
openapi_generator_jar = os.path.join(get_bin_dir(), openapi_url.split("/")[-1])
if os.path.exists(openapi_generator_jar) and os.path.getsize(openapi_generator_jar) :
    print(f"'{openapi_generator_jar}' already exists. It is no need to download it.")
else:
    openapi_generator_jar = download(url=openapi_url)

## generate
package_name='register_service'
genearte_api(package_name=package_name, swagger_url=swagger_url, openapi_generator_jar=openapi_generator_jar, templates=templates)

## rearrange
dst_folder = str(pathlib.Path(__file__).parent.parent.parent / f"clients/http/{package_name}")
move_directory_contents(f"{package_name}/{package_name}", dst_folder)
safe_remove_dir(package_name)