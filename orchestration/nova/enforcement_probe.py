#!/usr/bin/env python3
"""Measure native write/network refusal using harmless local controls, no models."""
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CHILD = r'''
import errno, json, socket, sys
from pathlib import Path
out = {}
try:
    Path(sys.argv[1]).write_text('changed')
    out['protected_write'] = 'allowed'
except OSError as exc:
    out['protected_write'] = 'denied' if exc.errno in (errno.EACCES, errno.EPERM) else 'other_error'
    out['write_errno'] = exc.errno
try:
    Path(sys.argv[2]).write_text('outbox-ok')
    out['outbox_write'] = 'allowed'
except OSError as exc:
    out['outbox_write'] = 'failed'
    out['outbox_errno'] = exc.errno
try:
    with socket.create_connection(('127.0.0.1', int(sys.argv[3])), timeout=3):
        out['local_connect'] = 'allowed'
except OSError as exc:
    out['local_connect'] = 'denied' if exc.errno in (errno.EACCES, errno.EPERM) else 'other_error'
    out['connect_errno'] = exc.errno
print(json.dumps(out))
'''


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go', type=Path, required=True)
    parser.add_argument('--friend', type=Path, required=True)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    lock = json.loads((ROOT / 'upstream.json').read_text())
    proof = dict(mode='native-wall-enforcement', enforced=False,
                 kernel=platform.release(), model_calls=0, external_connections=0,
                 live_fleet_tested=False, upstream_commit=lock['commit'],
                 nova_tools_version=lock['nova_tools_version'],
                 source_sha256={name: digest(ROOT / name)
                                for name in ('enforcement_probe.py', 'upstream.json')})
    try:
        with tempfile.TemporaryDirectory(prefix='nova-enforcement-') as temporary:
            scratch = Path(temporary)
            job, denied, home = (scratch / name for name in ('job', 'denied', 'home'))
            for path in (job, denied, home):
                path.mkdir()
            sentinel, outbox = denied / 'synthetic.txt', job / 'RESULT.txt'
            sentinel.write_text('preserved')
            env = {key: os.environ[key] for key in ('PATH', 'LANG', 'LC_ALL', 'TZ')
                   if key in os.environ}
            env['HOME'] = str(home)

            def run(command):
                return subprocess.run(command, cwd=job, env=env, text=True,
                                      capture_output=True, timeout=30)

            proof['binaries'] = {}
            for name in ('friend', 'sandbox'):
                binary = getattr(args, name).resolve()
                metadata = run([str(args.go.resolve()), 'version', '-m', str(binary)])
                expected = '\tmod\t' + lock['nova_tools_module'] + '\t' + lock['nova_tools_version'] + '\t'
                require(metadata.returncode == 0 and any(line.startswith(expected)
                        for line in metadata.stdout.splitlines()), 'Unpinned native binary: ' + name)
                proof['binaries'][name] = dict(sha256=digest(binary))

            checked = run([str(args.sandbox.resolve()), 'check', '--json'])
            facts = json.loads(checked.stdout).get('facts', {})
            proof['sandbox_check_exit'] = checked.returncode
            proof['sandbox_facts'] = {key: facts.get(key) for key in ('backend', 'abi', 'net')}
            # Listening only on loopback avoids external targets. The baseline
            # proves failures inside the wall cannot be blamed on a dead port.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
                listener.bind(('127.0.0.1', 0))
                listener.listen(4)
                port = listener.getsockname()[1]
                require(port not in (22, 443), 'Need a port the friend profile refuses')
                child = [str(Path(sys.executable).resolve()), '-I', '-c', CHILD,
                         str(sentinel), str(outbox), str(port)]
                baseline = run(child)
                require(baseline.returncode == 0, 'Baseline child failed')
                proof['outside_wall'] = json.loads(baseline.stdout)
                require(all(proof['outside_wall'][key] == 'allowed' for key in
                            ('protected_write', 'outbox_write', 'local_connect')),
                        'Unrestricted baseline did not demonstrate healthy controls')
                sentinel.write_text('preserved')
                outbox.unlink()
                wall = run([str(args.friend.resolve()), 'wall', '--profile', 'friend',
                    '--dir', str(job), '--deny', str(denied),
                    '--read', str(Path(sys.prefix).resolve()), '--', *child])
                proof['wall_exit'] = wall.returncode
                require(wall.returncode == 0, 'Native wall did not execute the enforcement child')
                proof['inside_wall'] = json.loads(wall.stdout)
                require(checked.returncode == 0 and facts.get('backend') == 'landlock'
                        and int(facts.get('abi', '0')) >= 4 and facts.get('net') == 'enforceable',
                        'Native filesystem/network enforcement backend unavailable')
                require(proof['inside_wall'].get('protected_write') == 'denied',
                        'Protected synthetic write was not denied')
                require(sentinel.read_text() == 'preserved', 'Protected sentinel changed')
                require(proof['inside_wall'].get('outbox_write') == 'allowed'
                        and outbox.read_text() == 'outbox-ok', 'Allowed outbox write failed')
                require(proof['inside_wall'].get('local_connect') == 'denied',
                        'Disallowed local TCP connection was not denied')
                proof['enforced'] = True
                proof['checks'] = ['healthy outside-wall controls', 'protected write refused',
                                   'own outbox writable', 'disallowed local TCP refused']
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired) as exc:
        proof['error'] = (type(exc).__name__ + ': ' + str(exc))[:1000]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(proof, indent=2))
    return 0 if proof['enforced'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
