import click
from os import getenv, path, makedirs
from src.config import loadConfig
from src.commands.update import updateCommand
from src.commands.install import installCommand
from src.commands.list_installed import listInstalledCommand
from src.commands.execute import executeCommand
from src.commands.search import searchCommand
from src.commands.upgrade import upgradeCommand
from src.commands.remove import removeCommand
from src.util import parseRepos
homedir = getenv('HOME')
dirs = {
    'root': f'{homedir}/.fenix',
    'repos': f'{homedir}/.fenix/repos',
    'apps': f'{homedir}/.fenix/apps',
    'config-file': f'{homedir}/.fenix/config.conf'
}

for _, (name, d) in enumerate(dirs.items()):
    if name != 'config-file' and not path.exists(d):
        makedirs(d)
if not path.exists(dirs['config-file']):
    with open(dirs['config-file'], 'w') as f:
        f.write("""
[repos.std]
Server = "https://raw.githubusercontent.com/farofaDeCachorro/fenix/main/repos/std.csv"
Type = "remote"
# example repo
# [repos.example]
# Server = "/home/username/.customrepo.csv"
# Type = "local"
        """)
config = loadConfig(dirs['config-file'])
repos = parseRepos(dirs)


@click.group('fenix')
def fenix():
    pass


@fenix.command()
def upgrade():
    upgradeCommand(dirs, repos)


@fenix.command()
@click.argument('app', nargs=-1)
def install(**kwargs):
    """Install program"""
    to_install_apps = kwargs.get('app')
    installCommand(repos, dirs, to_install_apps)


@fenix.command(context_settings={"ignore_unknown_options": True})
@click.argument('app')
@click.option('-a', '--args')
def execute(app, args):
    """run program"""
    executeCommand(dirs, (app, args))


@fenix.command()
@click.argument('app', nargs=-1)
def remove(**kwargs):
    """uninstall program"""
    to_remove_app = kwargs.get('app')
    removeCommand(dirs, to_remove_app)


@fenix.command()
def update(**kwargs):
    """update the repos."""
    updateCommand(config, dirs)


@fenix.command('list-installed')
def listInstalled():
    """list all programs installed"""
    listInstalledCommand(dirs)


@fenix.command()
@click.argument('query')
def search(**kwargs):
    """search for a application. tip 'all' for all apps."""
    searchCommand(dirs, repos, kwargs.get('query'))


if __name__ == '__main__':
    fenix()
