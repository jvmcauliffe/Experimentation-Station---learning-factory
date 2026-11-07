#!/usr/bin/env python3
"""Exercise real local Redis/Postgres configuration; no hook, worker or model."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
PG = 'postgres://nova_config@127.0.0.1:15432/nova'
SPRINT = '127.0.0.1:16379'
BUS = '127.0.0.1:16380'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bin-dir', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    lock = json.loads((ROOT / 'upstream.json').read_text())
    proof = dict(mode='native-service-config-smoke', ready=False,
                 upstream_commit=lock['commit'], nova_tools_version=lock['nova_tools_version'],
                 source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 model_calls=0, hook_presence_tested=False, route_rpc_tested=False,
                 live_fleet_tested=False, account_authentication_tested=False, steps=[])
    try:
        with tempfile.TemporaryDirectory(prefix='nova-service-config-') as scratch:
            env = {key: os.environ[key] for key in ('PATH', 'LANG', 'LC_ALL', 'TZ') if key in os.environ}
            env['HOME'] = scratch
            # Actor is configuration history only. No hook record is created or proved.
            def run(tool, words, must=True):
                r = subprocess.run([str((args.bin_dir / tool).resolve()), *words],
                                   cwd=scratch, env=env, capture_output=True, text=True, timeout=45)
                proof['steps'].append(dict(tool=tool, operation=' '.join(words[:2]), exit=r.returncode))
                if must and r.returncode:
                    raise ValueError(tool + ': ' + (r.stdout + r.stderr)[:1600])
                return r

            def config(*words):
                return json.loads(run('nova-config', [*words, '--pg', PG, '--json']).stdout)

            versions = {}
            for tool in ('nova-config', 'nova-sprint'):
                versions[tool] = run(tool, ['version']).stdout.strip()[:300]
            require(lock['nova_tools_version'] in versions['nova-config'], 'Wrong companion version')
            require('commit=' + lock['commit'] in versions['nova-sprint'], 'Wrong sprint commit')
            proof['versions'] = versions
            for name, port in (('sprint', 16379), ('bus', 16380)):
                with socket.create_connection(('127.0.0.1', port), timeout=5) as connection:
                    connection.sendall(b'*1\r\n$4\r\nPING\r\n')
                    require(connection.recv(64) == b'+PONG\r\n', name + ' Redis did not PONG')
            proof['redis_ping'] = dict(sprint=True, bus=True, separate_endpoints=True)
            config('migrate')
            second = config('migrate')
            require(second['facts']['applied'] == 0, 'Migration is not idempotent')
            proof['migration_reapply_count'] = 0
            config('machine', 'add', '127.0.0.1', '--user', 'runner', '--seat', 'canary',
                   '--slots', '1', '--width', '1', '--actor', 'canary')
            config('friend', 'add', 'canary', '--tiers', 'pro', '--width', '1',
                   '--roles', 'builder,reader', '--actor', 'canary')
            config('fleet', 'set', '--store', '127.0.0.1', '--coordinator', '127.0.0.1',
                   '--redis_port', '16379', '--pg_dsn', PG, '--bus', BUS, '--actor', 'canary')
            config('sprint', 'set', '--coordinator', 'canary', '--git_identity',
                   'Nova Canary <nova-canary@example.invalid>', '--max_attempts', '1', '--actor', 'canary')
            providers = config('provider', 'list')
            names = {item['fields']['name'] for item in providers.get('items', [])}
            config('provider', 'set' if 'subscription-codex' in names else 'add', 'subscription-codex',
                   '--billing', 'plan', '--funded', 'false', '--actor', 'canary')
            # Seed actor/fleet projections before route writes synchronously apply.
            config('apply', '--redis', SPRINT, '--actor', 'canary')
            # This route deliberately cannot execute or assert a funded account.
            config('route', 'add', 'canary-disabled', '--tier', 'pro', '--provider', 'subscription-codex',
                   '--harness', 'codex', '--model', 'unconfigured-canary', '--deadline', '30',
                   '--tokens', '1', '--usd', '0.01', '--billing', 'plan', '--enabled', 'false',
                   '--note', 'No authenticated account; service smoke only', '--actor', 'canary')
            config('apply', '--redis', SPRINT, '--actor', 'canary')
            checked = config('apply', '--redis', SPRINT, '--actor', 'canary', '--dry-run')
            kinds = [item['fields'] for item in checked.get('items', []) if item.get('kind') == 'kind']
            require(bool(kinds) and all(int(row[key]) == 0 for row in kinds
                                      for key in ('add', 'set', 'remove')), 'Redis projection has pending changes')
            proof['applied_kinds'] = [row['kind'] for row in kinds]
            route = config('route', 'show', 'canary-disabled')['items'][0]['fields']
            require(route['enabled'] == 'false', 'Canary route unexpectedly enabled')
            provider = config('provider', 'show', 'subscription-codex')['items'][0]['fields']
            require(provider['funded'] == 'false', 'Provider unexpectedly funded')
            proof['route_enabled'] = False
            proof['provider_funded'] = False
            # An actor-free read is supported without manufacturing a live hook.
            routes = run('nova-sprint', ['routes', '--redis', SPRINT, '--json'], must=False)
            proof['route_store_inspection_exit'] = routes.returncode
            proof['route_store_inspection_tested'] = routes.returncode == 0
            if routes.returncode:
                proof['route_store_limitation'] = (routes.stdout + routes.stderr)[:1000]
            proof['ready'] = True
            proof['limitations'] = ['Service/config readiness only; no sprint server, hook, authenticated account or worker.']
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        proof['error'] = (type(exc).__name__ + ': ' + str(exc))[:1800]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(proof, indent=2))
    return 0 if proof['ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
