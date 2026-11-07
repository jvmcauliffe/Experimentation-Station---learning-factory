#!/usr/bin/env python3
"""Build the pinned upstream engine. No model calls or live service setup."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go', required=True, type=Path, help='Go language executable, version 1.26.6 or newer')
    parser.add_argument('--runtime', required=True, type=Path, help='Untracked, user-owned installation directory')
    parser.add_argument('--source', type=Path, help='Reuse a clean checkout at the exact pinned commit')
    parser.add_argument('--cache', type=Path, help='Optional shared Go cache root')
    args = parser.parse_args()
    lock = json.loads((ROOT / 'upstream.json').read_text())
    go = str(args.go.resolve())
    version = subprocess.check_output([go, 'version'], text=True)
    match = re.search(r'go(\d+)\.(\d+)\.(\d+)', version)
    if not match or tuple(map(int, match.groups())) < tuple(map(int, lock['minimum_go'].split('.'))):
        parser.error('The Go language toolchain 1.26.6 or newer is required')
    runtime = args.runtime.resolve()
    runtime.mkdir(parents=True, exist_ok=True)
    source = args.source.resolve() if args.source else runtime / 'source'
    if not source.exists():
        subprocess.run(['git', 'clone', '--no-checkout', lock['repository'], str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'checkout', '--detach', lock['commit']], check=True)
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True)
    if head != lock['commit'] or dirty:
        parser.error('Source must be clean and at the exact upstream commit; no automatic reset')
    mod = (source / 'go.mod').read_text()
    if not re.search(re.escape(lock['nova_tools_module']) + r'\s+' + re.escape(lock['nova_tools_version']) + r'\s', mod):
        parser.error('Unexpected companion module dependency')
    cache = args.cache.resolve() if args.cache else runtime / 'cache'
    env = dict(os.environ, GOTOOLCHAIN='local', GOCACHE=str(cache / 'go-cache'),
               GOPATH=str(cache / 'go-path'), GOMODCACHE=str(cache / 'go-modules'))
    # Direct VCS is supported when a module proxy redirects to a blocked storage host.
    # TLS, go.sum verification and the inherited network policy remain enabled.
    env.setdefault('GOPROXY', 'direct')
    binary = runtime / 'bin' / 'nova-sprint'
    binary.parent.mkdir(exist_ok=True)
    subprocess.run([go, 'build', '-o', str(binary), './cmd/nova-sprint'], cwd=source, env=env, check=True)
    subprocess.run([str(binary), 'version'], check=True)
    companions = []
    for name in ('nova-bus', 'nova-hook', 'nova-friend', 'nova-config'):
        target = runtime / 'bin' / name
        subprocess.run([go, 'build', '-o', str(target), lock['nova_tools_module'] + '/cmd/' + name],
                       cwd=source, env=env, check=True)
        subprocess.run([str(target), 'version'], check=True)
        companions.append(str(target))
    print(json.dumps({'source_commit': head, 'go': version.strip(), 'binary': str(binary),
                      'companions': companions}))


if __name__ == '__main__':
    main()
