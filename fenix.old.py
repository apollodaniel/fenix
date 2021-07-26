import os
import csv
import sys
from fenix_install import *
import requests
from os import path
args = sys.argv  # get all args

homedir = os.environ['HOME']  # get home path of actual user

index = 0

chunk_size = 1048576
dirs = {
    'fenix-root': f'{homedir}/.fenix',
    'programs': f'{homedir}/.fenix/apps',
    'repos': f'{homedir}/.fenix/repos',
}


def createDirs():
    for d in dirs.values():
        if not path.exists(d):
            os.mkdir(d)


createDirs()
repository_path = f"{dirs['repos']}/official.csv"
apps_path = dirs['programs']

def getSize(fileobject):
    fileobject.seek(0, 2)  # move the cursor to the end of the file
    size = fileobject.tell()
    return size

 # update function
if "--update" in args:
    chunk_size = 1048576

    r = requests.get(
        "https://raw.githubusercontent.com/farofaDeCachorro/fenix/main/repository.csv", stream=True)

    total_size = int(r.headers['content-length'])

    with open(repository_path, 'wb') as f:
        for data in tqdm(iterable=r.iter_content(chunk_size=chunk_size), total=int(total_size/chunk_size), unit='MB'):
            f.write(data)
if "--help" in args:
    print("""List of basic commands:
--install (program name): install program
--remove (program name): remove program
--execute (program name): execute program
--list: list repository programs
--list -i: list installed programs
--update: update repository""")
else:
    for arg in args:
        if os.path.isfile(repository_path):
            # install function
            if arg == "--install":
                file_name = args[index + 1]
                # verifica se o aplicativo ta instalado, caso não ele instala
                if file_name in apps_path:
                    print(
                        f'{file_name} is already installed, please type "fenix --execute {file_name}" for execute him')
                else:
                    install(file_name, repository_path)

            # execute function
            if(arg == "--execute"):
                file_name = args[index + 1]

                # verifica se o programa existe, se sim executa, se não pede para ser instalado
                if file_name in apps_path:
                    app = f"{dirs['programs']}/{file_name}"
                    os.chmod(app, 777)
                    os.system(app)
                else:
                    print(
                        f"This application is not installed, you can install using fenix --install {file_name}")

            # remove function
            if arg == "--remove":
                try:
                    file_name = args[index + 1]
                    # verifica se o aplicativo esta instalado, se sim ele remove, se não fala que o aplicativo não esta instalado
                    if(file_name in apps_path):
                        os.system(f"rm {homedir}/.fenix/programs/{file_name}")
                        print("Program removed successfully")
                    else:
                        print(
                            f"This application is not installed, you can install using fenix --install {file_name}")
                except:
                    print("Enter the name of the application to be removed")

            # list function
            if arg == "--list":
                try:
                    parametro_intalado = args[index + 1]
                    if(parametro_intalado == "-i"):
                        if(len(apps_path) == 0):
                            print("There is nothing installed!")
                        else:
                            for aplicativos in apps_path:
                                file_size = os.stat(
                                    f'{homedir}/.fenix/programs/{aplicativos}')
                                file_size_mb = file_size.st_size / chunk_size
                                print(
                                    f"Program: {aplicativos} | Size: {'{:.2f}'.format(round(file_size_mb, 2))}MB")
                except:
                    with open(repository_path, 'r') as f:
                        file = csv.reader(f)
                        for lines in file:
                            print(lines[0])
            index += 1
        else:
            print("Please update repository with: fenix --update")
            break
