import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from twin import twin_environment

ROOT = Path(__file__).resolve().parent


class TwinIsolationTests(unittest.TestCase):
    def test_only_minimal_environment_is_inherited(self):
        source = {'PATH': '/bin', 'HOME': '/tmp', 'NOVA_SPRINT_SERVER': 'live:1',
                  'NOVA_OTHER_SETTING': 'live', 'OPENAI_API_KEY': 'PRIVATE',
                  'ANTHROPIC_AUTH_TOKEN': 'PRIVATE', 'GH_TOKEN': 'PRIVATE'}
        with mock.patch.dict(os.environ, source, clear=True):
            env = twin_environment()
        self.assertEqual(env, {'PATH': '/bin', 'HOME': '/tmp', 'NOVA_SPRINT_ACTOR': 'boss'})

    def test_home_is_replaced_for_native_processes(self):
        with mock.patch.dict(os.environ, {'HOME': '/real/home'}, clear=True):
            env = twin_environment('/scratch/home')
        self.assertEqual(env['HOME'], '/scratch/home')
        self.assertEqual(env['USERPROFILE'], '/scratch/home')

    def test_live_commands_and_single_dash_overrides_never_launch_binary(self):
        with tempfile.TemporaryDirectory() as scratch:
            command = [sys.executable, str(ROOT / 'twin.py'), '--binary', '/nonexistent-binary',
                       '--state', str(Path(scratch) / 'state'), '--']
            for words in (['run'], ['land'], ['fleet'], ['where', '-redis=live:1'],
                          ['where', '--redis', 'live:1'], ['tick', '--keys', 'SECRET']):
                with self.subTest(words=words):
                    done = subprocess.run(command + words, capture_output=True, text=True)
                    self.assertEqual(done.returncode, 2)
                    self.assertNotIn('FileNotFoundError', done.stderr)


if __name__ == '__main__':
    unittest.main()
