import os
import platform
import shutil
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings

from project_gen.scripts_to_generate_project.handle_dirs import get_bin_dir


OPENAPI_URL = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.16.0/openapi-generator-cli-7.16.0.jar"


def download(url: str = OPENAPI_URL) -> str:
    """
    :param url: file tp download
    :return: path where downloaded file is saved (bin/Script folder)
    """
    file_name = url.split("/")[-1]
    print(f"Start to download '{url}'...")
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        with requests.get(url, stream=True, timeout=100, verify=False) as response:
            response.raise_for_status()
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            if platform.system() != "Windows":
                os.chmod(file_name, 0o755)
    finally:
        warnings.resetwarnings()

    bin_dir = get_bin_dir()
    dest_path = os.path.join(bin_dir, file_name)
    shutil.move(file_name, dest_path)
    print(f"File is downloaded to '{dest_path}'")
    return dest_path


def init() -> str:
    openapi_generator_jar = os.path.join(get_bin_dir(), OPENAPI_URL.split("/")[-1])
    if os.path.exists(openapi_generator_jar) and os.path.getsize(openapi_generator_jar):
        print(
            f"'{openapi_generator_jar}' already exists. It is no need to download it."
        )
    else:
        openapi_generator_jar = download(url=OPENAPI_URL)

    return openapi_generator_jar
