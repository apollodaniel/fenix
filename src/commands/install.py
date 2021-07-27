from src.util import getPackage, echoErrorMessage, echoOkMessage
from os import system, listdir, remove
import requests
from tqdm import tqdm


def downloadApp(app_dir: str, app: dict, app_name: str):
    exec_path = f"{app_dir}/{app_name}@{app['version']}.app"
    r = requests.get(app['url'], stream=True)
    total_size = int(r.headers.get('content-length', 0))
    name = app_name
    name += ' '*(50-len(app_name))
    bar = tqdm(total=int(total_size), desc=name,
               ascii=True, unit_scale=True, unit="iB", dynamic_ncols=True)
    with open(exec_path, 'wb') as f:
        for data in r.iter_content(chunk_size=1024):
            bar.update(len(data))
            f.write(data)
    bar.close()
    system(f'chmod 777 {exec_path}')


def installCommand(repos: dict, dirs: dict, to_install_apps: str):
    apps = listdir(dirs['apps'])
    ins = []
    for to_install_app in to_install_apps:
        package_to_install = getPackage(repos, to_install_app)
        for f in apps:
            if f.split('@')[0] == to_install_app:
                echoOkMessage(f"{to_install_app} is installed -- reinstalling")
                remove(f"{dirs['apps']}/{f}")
        if not package_to_install:
            echoErrorMessage(f"target not found: {to_install_app}")
            return
        downloadApp(dirs['apps'], package_to_install, to_install_app)
        ins.append(to_install_app)
    echoOkMessage(f"{', '.join(ins)} has been installed.")
