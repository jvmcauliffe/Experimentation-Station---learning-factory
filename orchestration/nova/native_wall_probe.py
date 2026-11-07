#!/usr/bin/env python3
"""Probe the unmodified native wall; never start a model, fleet or service."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go', required=True, type=Path)
    parser.add_argument('--friend', required=True, type=Path)
    parser.add_argument('--sandbox', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    lock = json.loads((ROOT / 'upstream.json').read_text())
    proof = dict(mode='native-wall-readiness', ready=False, kernel=platform.release(),
                 upstream_commit=lock['commit'], nova_tools_version=lock['nova_tools_version'],
                 source_sha256={name: sha256(ROOT / name)
                                for name in ('native_wall_probe.py', 'upstream.json')},
                 model_calls=0, live_fleet_tested=False, managed_chat_delivery_tested=False)
    try:
        with tempfile.TemporaryDirectory(prefix='nova-native-wall-') as scratch:
            scratch = Path(scratch)
            job, denied, home = (scratch / name for name in ('job', 'denied', 'home'))
            for directory in (job, denied, home):
                directory.mkdir()
            env = {key: os.environ[key] for key in ('PATH', 'LANG', 'LC_ALL', 'TZ')
                   if key in os.environ}
            env['HOME'] = str(home)

            def run(command):
                return subprocess.run(command, cwd=job, env=env, capture_output=True,
                                      text=True, timeout=30)

            proof['binaries'] = {}
            for name in ('friend', 'sandbox'):
                binary = getattr(args, name).resolve()
                metadata = run([str(args.go.resolve()), 'version', '-m', str(binary)])
                expected = '\tmod\t' + lock['nova_tools_module'] + '\t' + lock['nova_tools_version'] + '\t'
                if metadata.returncode or not any(line.startswith(expected)
                                                 for line in metadata.stdout.splitlines()):
                    raise ValueError('Binary does not identify the pinned nova-tools module: ' + name)
                version = run([str(binary), 'version'])
                if version.returncode:
                    raise ValueError('Native version command failed: ' + name)
                proof['binaries'][name] = dict(sha256=sha256(binary), version=version.stdout.strip()[:300])

            checked = run([str(args.sandbox.resolve()), 'check', '--json'])
            check = json.loads(checked.stdout)
            facts = check.get('facts', {})
            proof['sandbox_check_exit'] = checked.returncode
            proof['sandbox_facts'] = {key: facts.get(key) for key in ('backend', 'abi', 'net', 'hosts', 'note')}
            # No profile changes or sandbox fallback. The native wall must actually
            # execute the harmless child; a dry-run or backend check is insufficient.
            wall = run([str(args.friend.resolve()), 'wall', '--profile', 'friend',
                        '--dir', str(job), '--deny', str(denied), '--', '/usr/bin/true'])
            proof['wall_exit'] = wall.returncode
            proof['wall_output'] = (wall.stdout + wall.stderr)[:4000]
            try:
                abi = int(facts.get('abi', ''))
            except (ValueError, TypeError):
                abi = 0
            proof['ready'] = (checked.returncode == 0 and facts.get('backend') == 'landlock'
                              and abi >= 4 and wall.returncode == 0)
            if not proof['ready']:
                proof['blocker'] = 'Native Landlock wall readiness was not demonstrated; no worker may start.'
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        proof['error'] = (type(exc).__name__ + ': ' + str(exc))[:1000]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(proof, indent=2))
    return 0 if proof['ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
