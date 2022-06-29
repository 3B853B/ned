#!/usr/bin/env python3

import os
import sys

from pathlib import Path


def config() -> None:
    shell = os.environ.get('SHELL')
    home = Path.home()

    path_variables = {
        'platform_tools': f'{home}/Library/Android/sdk/platform-tools',
        'emulator': f'{home}/Library/Android/sdk/emulator'
    }

    if 'zsh' in shell:
        filename = '.zshrc'
    elif 'bash' in shell:
        filename = '.bashrc'
    else:
        sys.exit(os.EX_SOFTWARE)

    with open(home.joinpath(filename), 'a') as file:
        file.write('\n# Android SDK Variables\n')
        path_appendix = ''
        for key, value in path_variables.items():
            file.write(f'{key.upper()}="{value}"\n')
            path_appendix += f':${key.upper()}'

        file.write(f'PATH="$PATH{path_appendix}"\n')


if __name__ == '__main__':
    config()
    sys.exit(os.EX_OK)
