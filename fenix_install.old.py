from tqdm import tqdm
import requests
import os
import csv
import sys

homedir = os.environ['HOME']

def Prepara_arquivo(file_path):
    os.system(f"chmod 777 {file_path} && ./{file_path}")

def Baixa_arquivo(url, filename):

    chunk_size = 1048576

    r = requests.get(url, stream = True)
    
    total_size = int(r.headers['content-length'])
    
    with open(f'{homedir}/.fenix/programs/{filename}', 'wb') as f:
        try:
            for data in tqdm(iterable = r.iter_content(chunk_size = chunk_size), total = int(total_size/chunk_size), unit = 'MB'):
                    f.write(data)
        except KeyboardInterrupt:
            print("Cancelling installation...")
            os.system(f"rm -r {homedir}/.fenix/programs/{filename} ")


def install(file_name, repository_path):
    with open(repository_path, 'r') as f:
        file = csv.reader(f)

        for lines in file:
            if(file_name in lines[0]):
                print(f"Installing {lines[0]}, please wait!")
                Baixa_arquivo(lines[1], lines[0])
