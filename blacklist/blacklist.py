from builtins import *

import os
from glob import glob
from itertools import chain
import re
import click
import json

try:
    import readline
except ImportError:
    import pyreadline as readline


def blacklist(root, matches, filters=('*',), is_delete_mode=False, is_dry_run=False, ignored=("?")):
    menu = """
    **Options**
    [u] update              [d] delete 
    [i] ignore match        [q] quit
    """

    def rlinput(prompt, prefill=''):
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()

    def indent(level):
        return "    " * level

    def prompt_action(index):
        for i in range(index - 3, index + 3):
            if 0 <= i < len(lines):
                click.secho("{}".format(i + 1).rjust(4), nl=False, fg="yellow")
                if i == index:
                    click.secho(indent(1) + "{}".format(lines[i]), nl=False, fg='cyan')
                else:
                    click.secho(indent(1) + "{}".format(lines[i]), nl=False, fg='white')

        click.echo(menu)
        while True:
            action = click.prompt(indent(2) + "What to do?", default="i", show_default=True, type=str)
            if action == 'u':
                new_line = rlinput(indent(2) + "Change to: ", line)
                lines[index] = new_line + "\n"
                return
            elif action == 'd':
                lines.pop(index)
                return
            elif action == 'i':
                return
            elif action == 'q':
                return "exit"
            # elif action == 'b':
            #     click.echo(indent(3)+"Sorry but this hasn't yet been implemented :(")
            else:
                click.echo(indent(3) + "Ups... that's not a valid option")

    _files = []
    for _f in filters:
        _files += (chain.from_iterable(glob(os.path.join(x[0], _f)) for x in os.walk(root)))
    # files = [file for file in _files if (os.path.isfile(file) and [i not in file for i in ignored ])]
    files = [file for file in _files if (os.path.isfile(file) and not list(filter(lambda i: i in file,ignored)))]
    for _file in files:
        with open(_file) as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                for match in matches:
                    found = re.search(match, line)
                    if found:
                        click.echo("\nFound: ", nl=False)
                        click.secho(found.group(0), fg='green')
                        click.secho("On file: ", nl=False)
                        click.secho(_file + ", line " + str(index + 1) + ".\n", fg='green')
                        if is_dry_run:
                            continue
                        elif is_delete_mode:
                            click.echo(indent(1) + "DELETED!")
                            lines.pop(index)
                        else:
                            if prompt_action(index) == "exit":
                                with open(_file, 'w') as f:
                                    f.writelines(lines)
                                return

        with open(_file, 'w') as f:
            f.writelines(lines)
    click.echo("All files checked.")


@click.command()
@click.argument('path')
@click.option('-m', '--match', help="Expresion to match (Regular expresion).")
@click.option('-f', '--filter', 'filter_', help="Filter files to check (Regular expresion).")
@click.option('-c', '--config-file', help="Load a configuration file.")
@click.option('--delete', 'is_delete_mode', is_flag=True, help="Execute the Delete option for all matches.")
@click.option('--dry-run', 'is_dry_run', is_flag=True, help="Display matches but take no action")
def cli(path, match, filter_, config_file, is_delete_mode, is_dry_run):
    if not config_file:
        if not match:
            match = click.prompt("Expression to match against (Regular expression)")

        blacklist(path, (match,), (filter_,) if filter_ else ('*',), is_delete_mode, is_dry_run)
    else:
        config = json.load(open(config_file))
        try:
            blacklist(
                path,
                tuple(config['matches']),
                tuple(config['filters']) if 'filters' in config else ('*',),
                is_delete_mode,
                is_dry_run,
                tuple(config['ignored']) if 'ignored' in config else (None,)
            )
        except KeyError:
            click.echo("Error: There is no 'matches' specified on the given configuration file.")

    click.echo("\n    Bye.")


if __name__ == "__main__":
    cli()
