from os import listdir
from src.util import echoOkMessage


def listInstalledCommand(dirs: dict):
    for d in listdir(dirs['apps']):
        split = d.split('@')
        name = split[0]
        version = split[1].replace('.app', '')
        echoOkMessage(f'name: {name}, version: {version}')
