#!/usr/bin/env python3
"""Exercise upstream's local twin, not paid agents or real Git landing."""
import argparse
from datetime import datetime, timezone
import json
import hashlib
from pathlib import Path
import subprocess
import tempfile

from twin import twin_environment

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    lock = json.loads((ROOT / 'upstream.json').read_text())
    binary = str(args.binary.resolve())
    version = subprocess.check_output([binary, 'version'], text=True).strip()
    if 'commit=' + lock['commit'] not in version:
        parser.error('Binary is not the pinned upstream revision')
    transcript = []
    # Every operation starts a fresh process and reopens the file-backed state.
    # No server, credentials, external worker or model call is involved.
    env = twin_environment()
    with tempfile.TemporaryDirectory(prefix='nova-twin-') as scratch:
        state = 'mem:' + str(Path(scratch) / 'sprint.twin')

        def run(*words, refused=False):
            result = subprocess.run([binary, words[0], '--redis', state, *words[1:]],
                                    env=env, text=True, capture_output=True, timeout=30)
            transcript.append(dict(command=list(words), exit_code=result.returncode,
                                   stdout=result.stdout, stderr=result.stderr))
            if refused:
                assert result.returncode != 0 and refused in (result.stdout + result.stderr).lower(), transcript[-1]
            else:
                assert result.returncode == 0, transcript[-1]
            return result.stdout

        run('init', '--readers', 'reader-m2', '--members', 'm1:1,m2:1')
        run('add', '--stream', 's1', '--count', '1', '--one')
        run('start')
        run('tick')
        run('tick')
        run('take', '--as', 'm1', '--epoch', '0')
        run('finish', '--as', 'm1', 's1-1.w1@99', '--epoch', '0', '--report', 'simulated work', refused='stale')
        before = json.loads(run('where', '--json'))
        assert before['landed'] == 0 and before['tables']['work']['s1']['working'] == '1'
        run('finish', '--as', 'm1', 's1-1.w1@1', '--epoch', '0', '--report', 'simulated work')
        run('tick')
        # An early merge may return a no-op, but must never land unreviewed work.
        run('merge', '--stream', 's1', '--batch', '1', refused='nothing queued')
        unreviewed = json.loads(run('where', '--json'))
        assert unreviewed['landed'] == 0 and unreviewed['tables']['work']['s1']['review'] == '1'
        run('take', '--as', 'm2', '--epoch', '0')
        run('read', '--as', 'm2', '--ok', 's1-1.r1.m2@1', '--epoch', '0')
        run('tick')
        reviewed = json.loads(run('where', '--json'))
        assert reviewed['landed'] == 0 and reviewed['tables']['work']['s1']['merging'] == '1'
        run('merge', '--stream', 's1', '--batch', '1')
        run('tick')
        final = json.loads(run('where', '--json'))
        assert final['landed'] == 1 and final['all'] == 1
        assert final['width'] == 2
        # An explicitly failed finish cannot simply be overwritten. Upstream's
        # special deadline-failed late-report recovery is a distinct path; this
        # test must not claim to cover that path or mint any packet receipt.
        state = 'mem:' + str(Path(scratch) / 'late.twin')
        run('init', '--readers', 'reader-m2', '--members', 'm1:1,m2:1')
        run('add', '--stream', 's1', '--count', '1', '--one')
        run('start')
        run('tick')
        run('tick')
        run('take', '--as', 'm1', '--epoch', '0')
        run('finish', '--as', 'm1', 's1-1.w1@1', '--epoch', '0', '--failed', '--report', 'simulated interrupted worker')
        run('finish', '--as', 'm1', 's1-1.w1@1', '--epoch', '0', '--report', 'late recovered simulated result', refused='not working')
        late = json.loads(run('where', '--json'))
        assert late['landed'] == 0
    proof = dict(observed_at=datetime.now(timezone.utc).isoformat(), source_commit=lock['commit'],
                 binary_version=version, mode='upstream-local-twin', simulated_landing=True,
                 model_calls=0, paid_dispatches=0, live_session_delivery='not tested',
                 source_sha256={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                for name in ('smoke.py', 'twin.py', 'bootstrap.py', 'upstream.json')},
                 binary_sha256=hashlib.sha256(args.binary.read_bytes()).hexdigest(),
                 checks=['state persists across separate CLI processes', 'stale generation refused',
                         'finish moves to independent reader', 'review precedes simulated landing',
                         'unreviewed merge cannot land a card',
                         'explicit failed finish cannot be overwritten by a late result',
                         'one simulated card landed', 'two one-slot simulated members'],
                 transcript=transcript)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps({key: value for key, value in proof.items() if key != 'transcript'}, indent=2))


if __name__ == '__main__':
    main()
