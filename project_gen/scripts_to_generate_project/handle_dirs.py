import os
import pathlib
import shutil
import time
from pathlib import Path


def get_bin_dir() -> str:
    venv_path = os.environ.get('VIRTUAL_ENV')
    if os.name == 'nt':
        bin_dir = os.path.join(venv_path, 'Scripts')
    else:
        bin_dir = os.path.join(venv_path, 'bin')
    return bin_dir


def safe_remove_dir(
        folder_name,
        max_attempts=3,
        delay=1
):
    """Safe dir removing with retries for Windows"""
    path = Path(folder_name)

    if not path.exists():
        return True

    # wait some time to release files
    time.sleep(delay)

    for attempt in range(max_attempts):
        try:
            shutil.rmtree(path)
            print(f"Directory '{path.absolute()}' is removed successfully")
            return True
        except PermissionError:
            if attempt < max_attempts - 1:
                print(f"Retry {attempt + 1} fails, another is in  {delay} sec...")
                time.sleep(delay)
                # garbage collection
                import gc
                gc.collect()
            else:
                print(f"Fail to remove dir '{path.absolute()}' after {max_attempts} attempts")
                return False
    return False


def move_directory_contents(
        src,
        dst
):
    """Move contents of src directory to dst, then remove src"""
    print(f"Moving contents from {src} to {dst}")
    cur_script_name = os.path.basename(__file__)

    # Create dst if not exists
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)

    # Move contents
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        # Skip files with script to generate project
        if Path.cwd().name == 'scripts_to_generate_project':
            continue

        # Skip .git and script files
        if item in ['openapi-generator-cli-7.16.0.jar', cur_script_name, '.gitignore', 'LICENSE', 'poetry.lock',
                    'pyproject.toml', 'README.md', 'testproject.toml', '.git', '.venv', '.idea', '__pycache__']:
            print(f'Skipping "{item}"')
            continue

        try:
            # If destination exists, remove it first
            if os.path.exists(dst_path):
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                    print(f"WARNING directory '{dst_path}' is removed")
                else:
                    os.remove(dst_path)
            # Move the item
            shutil.move(src_path, dst_path)
            print(f"Moved: {item}")
        except Exception as e:
            print(f"Error moving {item}: {e}")

    print("\n" + "=" * 50)
    print(f"\nProject location: '{dst.absolute()}'")


# def move_files(package_name: str) -> None:
#     client_dir = f"clients/http/{package_name}"
#     if os.path.exists(client_dir):
#         shutil.rmtree(client_dir)
#     shutil.move(f"{package_name}/{package_name}", client_dir)
#     shutil.rmtree(package_name)

def replace_imports_in_files(
        directory: str,
        package_name: str
) -> None:
    from_search_pattern = f"from {package_name}"
    import_search_pattern = f"import {package_name}"
    replace_pattern = f"clients.http.{package_name}"
    path = pathlib.Path(directory)
    for file_path in path.rglob("*.py"):
        print(f"Start fixing file '{file_path}'")
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            line = line.replace(from_search_pattern, f"from {replace_pattern}")
            line = line.replace(import_search_pattern, f"import {replace_pattern}")
            line = line.replace(
                f"getattr({package_name}.models, klass)",
                f"getattr(clients.http.{package_name}.models, klass)"
            )
            updated_lines.append(line)

        with file_path.open("w", encoding="utf-8") as file:
            file.writelines(updated_lines)
