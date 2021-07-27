from os import listdir
from src.util import getPackage
from src.commands.install import downloadApp
from src.util import echoOkMessage
from os import remove


def upgradeCommand(dirs: dict, repos: dict):
    print("checking for updates...")
    updates = {}
    for app in listdir(dirs['apps']):
        split = app.split('@')
        name = split[0]
        version = split[1].replace('.app', '')
        package = getPackage(repos, name)
        if package:
            if package['type'] == 'Version':
                local_version: str = version
                remote_version: str = package['version']
                local_version_splitted = local_version.split('.')
                remote_version_splitted = remote_version.split('.')
                try:
                    for i in range(0, len(remote_version_splitted)):
                        if local_version_splitted[i] is not None and remote_version_splitted[i] is not None:
                            if local_version_splitted[i] < remote_version_splitted[i]:
                                if updates.get(app) is None:
                                    updates[app] = package
                except:
                    pass

            if package['type'] == 'hash':
                if package['version'] != version:
                    updates.append(package)
    if len(updates) > 0:
        echoOkMessage(f'{len(updates)} updates found.')
        for _, (package_name, package) in enumerate(updates.items()):
            n = package_name.split('@')[0]
            remove(f"{dirs['apps']}/{package_name}")
            downloadApp(dirs['apps'], package, n)
        echoOkMessage('done.')
    else:
        echoOkMessage('nothing to do.')
