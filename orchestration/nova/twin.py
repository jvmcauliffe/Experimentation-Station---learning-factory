#!/usr/bin/env python3
"""Use upstream Nova's file-backed local twin, explicitly isolated from live seats."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

SAFE_COMMANDS = {'init', 'add', 'start', 'stop', 'tick', 'where', 'card', 'log',
                 'take', 'finish', 'read', 'merge', 'queue'}


def twin_environment(home=None):
    """Give the simulation no inherited Nova configuration or model credentials."""
    allowed = {'PATH', 'HOME', 'USER', 'LANG', 'LC_ALL', 'TZ', 'TMPDIR', 'TEMP', 'TMP',
               'SYSTEMROOT', 'WINDIR'}
    env = {key: value for key, value in os.environ.items() if key in allowed}
    if home is not None:
        env['HOME'] = str(home)
        env['USERPROFILE'] = str(home)
    env['NOVA_SPRINT_ACTOR'] = 'boss'
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--state', required=True, type=Path)
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Native nova-sprint command after --')
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('Supply a native command, for example -- where --json')
    if command[0] not in SAFE_COMMANDS:
        parser.error('Only finite local-twin workflow commands are supported; no run, land, fleet or session setup')
    if any(x.startswith('-') and x.lstrip('-').split('=')[0] in
           {'redis', 'server', 'actor', 'keys', 'decide', 'listen', 'repo-dir', 'check'} for x in command):
        parser.error('Connection, credential and execution overrides are not allowed through the local twin wrapper')
    state = args.state.resolve()
    state.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='nova-twin-command-') as scratch:
        return subprocess.run([str(args.binary.resolve()), command[0], '--redis', 'mem:' + str(state),
                               *command[1:]], cwd=scratch, env=twin_environment(scratch)).returncode


if __name__ == '__main__':
    raise SystemExit(main())
