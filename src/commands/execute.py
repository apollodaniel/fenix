from os import listdir, system
def executeCommand(dirs: dict, app_name: str):
    for d in listdir(dirs['apps']):
        if d.startswith(app_name):
            system(f"{dirs['apps']}/{d}")