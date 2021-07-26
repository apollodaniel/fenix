from src.util import echoOkMessage
from os import listdir
from colorama import ansi


def getInstalledApps(app_dir: str) -> list[str]:
    res = []
    for d in listdir(app_dir):
        res.append(d.split('@')[0])
    return res


def searchCommand(dirs: dict, repos: dict, query: str):
    installed_apps = getInstalledApps(dirs['apps'])
    for _, (repo_name, repo) in enumerate(repos.items()):
        for _, (package, data) in enumerate(repo.items()):
            s = f"{ansi.Fore.CYAN}{repo_name}{ansi.Fore.RESET}/{package} {ansi.Fore.YELLOW}{data['version']}{ansi.Fore.LIGHTGREEN_EX}{ ' [Installed]' if package in installed_apps else ''}{ansi.Fore.RESET}"
            if query == 'all':
                echoOkMessage(s)
            elif query == package:
                echoOkMessage(f'exact match: {s}')
            elif query in package:
                echoOkMessage(s)
            
