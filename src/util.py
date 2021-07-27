from os import listdir
import csv
from colorama import ansi

def parseRepos(dirs: dict) -> dict:
    result = {}
    for repo in listdir(dirs['repos']):
        result[repo.replace('.csv', '')] = {}
        with open(f"{dirs['repos']}/{repo}") as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == 'program':
                    continue
                result[repo.replace('.csv', '')][line[0].strip()] = {
                    'version': line[1].strip(),
                    'url': line[2].strip(),
                    'type': line[3].strip(),
                }
    return result
def echoErrorMessage(message: str) -> None:
    print(f"{ansi.Style.BRIGHT}{ansi.Fore.RED}error: {ansi.Fore.RESET}{message}")
def echoOkMessage(message: str) -> None:
    print(f"{ansi.Style.BRIGHT}{ansi.Fore.LIGHTBLUE_EX}ok: {ansi.Fore.RESET}{message}")
def getPackage(repos: dict, name: str) -> dict: 
    for _, (_, repo) in enumerate(repos.items()):
        for _, (package_name, package) in enumerate(repo.items()):
            if package_name == name:
                return package
