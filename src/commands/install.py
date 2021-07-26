from src.util import getPackage, echoErrorMessage, echoOkMessage
from os import system
import requests
from tqdm import tqdm



def downloadApp(app_dir: str, app: dict, app_name: str):
    exec_path = f"{app_dir}/{app_name}@{app['version']}.app"
    r = requests.get(app['url'], stream=True)
    total_size = int(r.headers.get('content-length', 0))
    bar = tqdm(total=int(total_size), desc=app_name,
               ascii=True, unit_scale=True, unit="iB")
    with open(exec_path, 'wb') as f:
        for data in r.iter_content(chunk_size=1024):
            bar.update(len(data))
            f.write(data)
    bar.close()
    system(f'chmod 777 {exec_path}')

    echoOkMessage(f'{app_name} has been installed.')


def installCommand(repos: dict, dirs: dict, to_install_app: str):
    package_to_install = getPackage(repos, to_install_app)
    if not package_to_install:
        echoErrorMessage(f"target not found: {to_install_app}")
    downloadApp(dirs['apps'], package_to_install, to_install_app)
