import toml
def loadConfig(path: str) -> dict:
    tml = None
    with open(path, 'r') as f:
        tml = toml.loads(f.read()) 
    return tml     