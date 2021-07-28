from os import listdir, system
from src.util import echoErrorMessage
def executeCommand(dirs: dict, args: tuple):
    for d in listdir(dirs['apps']):
        if d.startswith(args[0]):
            command = f"{dirs['apps']}/{d}"
            try:
                if args[1] is not None:
                    command += " " + args[1]
            except:
                pass
            system(command)
            return
    echoErrorMessage(f"{args[0]} isn't not installed.")

