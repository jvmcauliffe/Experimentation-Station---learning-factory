#!/usr/bin/env python3
"""Use upstream Nova's file-backed local twin, explicitly isolated from live seats."""
import argparse
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--state', required=True, type=Path)
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Native nova-sprint command after --')
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('Supply a native command, for example -- where --json')
    if any(x.split('=')[0] in {'--redis', '--server', '--actor'} for x in command):
        parser.error('Connection and actor overrides are not allowed through the local twin wrapper')
    state = args.state.resolve()
    state.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for key in ('NOVA_SPRINT_SERVER', 'NOVA_SPRINT_REDIS', 'NOVA_REDIS_ADDR', 'NOVA_BUS_REDIS'):
        env.pop(key, None)
    env['NOVA_SPRINT_ACTOR'] = 'boss'
    return subprocess.run([str(args.binary.resolve()), command[0], '--redis', 'mem:' + str(state),
                           *command[1:]], env=env).returncode


if __name__ == '__main__':
    raise SystemExit(main())
