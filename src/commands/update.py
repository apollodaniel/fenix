from tqdm import tqdm
import requests
from src.util import echoOkMessage
def updateCommand(config: dict, dirs: dict):
    for _, (name, repo) in enumerate(config['repos'].items()):
        
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