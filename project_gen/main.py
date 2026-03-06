import click

from project_gen.scripts_to_generate_project.download import init
from project_gen.scripts_to_generate_project.generate import generate

from project_gen.scripts_to_generate_project.utils import setup

swagger_url = "http://185.185.143.231:8085/register/openapi.json"
templates = "C:\\Users\\skolp\\PycharmProjects\\openapi-generator\\modules\\openapi-generator\\src\\main\\resources\\python"


package_name='register_service'


@click.group()
def cli() -> None:...

@cli.command("setup")
@click.option("--template", "-t", required=False, default=None)
def setup_command(template: str | None) -> None:
    setup(template=template)
    init()

@cli.command("generate")
def generate_command() -> None:
    generate()

@cli.command("init")
def init_command() -> None:
    init()

cli.add_command(generate_command)
cli.add_command(setup_command)
cli.add_command(init_command)

if __name__ == '__main__':
    cli()


