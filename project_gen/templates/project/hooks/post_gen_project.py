import os
import shutil
import subprocess
from pathlib import Path, PurePath
from tempfile import TemporaryDirectory


def _move_single_file(src_dir: PurePath, dst_dir: PurePath, file_name: str):
    shutil.move(
        str(src_dir.joinpath(file_name)),
        dst_dir.joinpath(file_name),
        copy_function=lambda x, y: shutil.copytree(
            x, y, dirs_exist_ok=True, copy_function=shutil.copy2
        ),
    )


def move_directory_contents(src: PurePath, dst: PurePath):
    temp_dir = TemporaryDirectory()
    temp_dir_path = Path(temp_dir.name)

    directory_contents = os.listdir(src)
    for item in directory_contents:
        _move_single_file(src, temp_dir_path, item)

    for item in directory_contents:
        _move_single_file(temp_dir_path, dst, item)

    os.removedirs(src)


# cookiecutter.exceptions.FailedHookException: #shutil.Error


def init_poetry():
    subprocess.run(["poetry", "install", "--no-root"])


def init_pre_commit():
    subprocess.run(["poetry", "add", "pre-commit"])
    subprocess.run(["poetry", "run", "pre-commit", "install"])
    subprocess.run(["poetry", "run", "pre-commit", "autoupdate"])


if __name__ == "__main__":
    # if "{{ cookiecutter.use_current_directory }}".lower() == "y":
    #     src = Path.cwd()
    #     move_directory_contents(src, src.parent)

    init_poetry()
    init_pre_commit()
