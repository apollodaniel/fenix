from os import listdir, remove
from src.util import echoErrorMessage, echoOkMessage
def removeCommand(dirs: dict, apps_to_remove: tuple):
    apps = listdir(dirs['apps'])
    apps_tmp = {}
    for app in apps:
        apps_tmp[app.split('@')[0]] = app
    apps = apps_tmp
    removed_apps = []
    for app in apps_to_remove:
        if app not in apps:   
            echoErrorMessage(f"{app} isn't not installed.")
            return
        for _, (app_name, path) in enumerate(apps.items()):
            if app_name in apps_to_remove:
                if app_name not in removed_apps:
                    remove(f"{dirs['apps']}/{path}")
                    echoOkMessage(f"{app_name} has been removed.")
                    removed_apps.append(app_name)
                