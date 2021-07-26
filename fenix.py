import click
from os import getenv, path, makedirs
from src.config import loadConfig
from src.commands.update import updateCommand
from src.commands.install import installCommand
from src.commands.execute import executeCommand
from src.util import parseRepos
homedir = getenv('HOME')
dirs = {
    'root': f'{homedir}/.fenix',
    'repos': f'{homedir}/.fenix/repos',
    'apps': f'{homedir}/.fenix/apps',
    'config-file': f'{homedir}/.fenix/config.conf'
}
repos = parseRepos(dirs)
for _, (name, d) in enumerate(dirs.items()):
    if name != 'config-file' and not path.exists(d):
        makedirs(d)
if not path.exists(dirs['config-file']):
    with open(dirs['config-file'], 'w') as f:
        f.write("""
        [repos.std]
Server = "https://raw.githubusercontent.com/yxqsnz/fenix/main/repos/std.csv"
Type = "remote"
# example repo
# [repos.example]
# Server = "~/customrepo.csv"
# Type = "local"
        """)
config = loadConfig(dirs['config-file'])


@click.group('fenix')
def fenix():
    pass


@fenix.command()
@click.argument('app')
def install(**kwargs):
    """Install an appImage in repos."""
    to_install_app = kwargs.get('app')
    installCommand(repos, dirs, to_install_app)
@fenix.command()
@click.argument('app')
def execute(**kwargs):
    to_install_app = kwargs.get('app')
    executeCommand(dirs, to_install_app)
@fenix.command()
@click.argument('app')
def remove(**kwargs):
    to_remove_app = kwargs.get('app')


@fenix.command()
def update(**kwargs):
    """update the repos."""
    updateCommand(config, dirs)


if __name__ == '__main__':
    fenix()
