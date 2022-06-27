#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


def config(username: str, email: str, signing_key: str, scope: str) -> None:
    try:
        configurations = {
            'username': ['user.name', username],
            'email': ['user.email', email],
            'signing_key': ['user.signingkey', signing_key],
            'gpg_sign': ['commit.gpgsign', 'true'],
            'default_branch': ['init.defaultBranch', 'main']
        }

        for param in configurations.values():
            cmd = ['git', 'config', f'--{scope}']
            cmd.extend(param)

            subprocess.run(cmd, check=True, timeout=5)

        shell = os.environ.get('SHELL')
        home = Path.home()
        path_variable = 'export GPG_TTY=$(tty)'

        if 'zsh' in shell:
            with open(home.joinpath('.zshrc'), 'r+') as file:
                if path_variable in file.read():
                    sys.exit(os.EX_OK)
                else:
                    file.write(path_variable)

        elif 'bash' in shell:
            with open(home.joinpath('.bashrc'), 'r+') as file:
                if path_variable in file.read():
                    sys.exit(os.EX_OK)
                else:
                    file.write(path_variable)

    except subprocess.CalledProcessError as ex:
        print(f'Process Error: {ex}')

    except subprocess.TimeoutExpired as ex:
        print(f'Process Timeout: {ex}')

    except FileNotFoundError as ex:
        print(f'File not found: {ex}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='git_helper',
        usage='%(prog)s -u Clancy -e clancy@banditos.com '
              '-k clancy@banditos.com -s global',
        description='Simple Git Configuration Script',
        allow_abbrev=False
    )

    parser.add_argument(
        '-u',
        metavar='',
        help='set your username',
        required=True,
        dest='username'
    )

    parser.add_argument(
        '-e',
        metavar='',
        help='set your email',
        required=True,
        dest='email'
    )

    parser.add_argument(
        '-k',
        metavar='',
        help='set your PGP key',
        required=True,
        dest='pgp_key'
    )

    parser.add_argument(
        '-s',
        choices=['local', 'global', 'system'],
        help='set the config scope',
        required=True,
        dest='scope'
    )

    args = parser.parse_args()

    config(
        username=args.username,
        email=args.email,
        signing_key=args.pgp_key,
        scope=args.scope
    )
