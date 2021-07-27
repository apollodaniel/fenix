from tqdm import tqdm

import requests
from os import path
from src.util import echoOkMessage, echoErrorMessage
def updateCommand(config: dict, dirs: dict):
    for _, (name, repo) in enumerate(config['repos'].items()):
        if repo['Type'] == 'remote':
            r = requests.get(repo['Server'], stream=True)
            total_size = int(r.headers.get('content-length', 0))
            bar = tqdm(total=int(total_size), desc=name,
               ascii=True, unit_scale=True, unit="iB")

            with open(f"{dirs['repos']}/{name}.csv", 'wb') as f:
                for data in r.iter_content(chunk_size=1024):
                    bar.update(len(data))
                    f.write(data)
            bar.close()
            echoOkMessage(f'{name} updated.')
        else:
            if not path.exists(repo['Server']):
                echoErrorMessage(f"file {repo['Server']} does not exist.")
                return
            with open(repo['Server'], 'r') as src:
                with open(f"{dirs['repos']}/{name}.csv", 'w') as dest:
                    dest.write(src.read())
            echoOkMessage(f'{name} updated.')
            