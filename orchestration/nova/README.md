# Nova orchestration adoption

Use the upstream Nova Sprint engine rather than implement another scheduler.
The exact source and companion dependency are pinned in `upstream.json`.
Upstream is MIT-licensed; the build retains its source checkout and licence.
No Nova source is copied into this repository.

## What works here

The pinned engine builds on Linux amd64 with Go 1.26.6. The local twin passes
a worker → independent simulated reviewer → simulated landing sequence,
preserves state across fresh CLI processes and refuses stale-generation results.
`evidence/local-twin.json` contains the actual commands, outputs and limitations.
The twin invokes no models, makes no real repository merge and does not prove
unattended operation or live chat delivery. Its simulated workers are two
one-slot members. Each command advances the twin; nothing ticks in the background.

## Build the actual upstream binary

Use the Go language toolchain, not the unrelated `/usr/bin/go` program present
in the initial cloud image. Supply an existing user-owned Go 1.26.6+ executable:

```sh
python3 orchestration/nova/bootstrap.py \
  --go /path/to/go/bin/go --runtime /path/to/untracked/nova-runtime
```

The installer fetches the pinned Git revision, checks for a clean exact checkout,
verifies the companion version and builds `nova-sprint`, `nova-bus`, `nova-hook`,
`nova-friend` and `nova-config` with local dependency caches.
`--source /path/to/clean/pinned/nova-sprint` reuses a checkout, and
`--cache /path/to/cache-root` reuses the three Go cache directories. Direct VCS
fetching is the default because this environment's module-proxy ZIP redirect was
denied; TLS and module verification remain enabled. No system configuration,
global Git configuration, credentials or model access is changed.

## Exercise the native workflow

```sh
python3 orchestration/nova/smoke.py \
  --binary /path/to/nova-runtime/bin/nova-sprint \
  --output /path/to/untracked/local-twin-proof.json
```

This runs a fresh isolated twin and checks state transitions, independent
simulated review and stale-result refusal. It does not mark actual project
work accepted. For direct use of the native CLI against a persistent local twin:

```sh
python3 orchestration/nova/twin.py --binary /path/to/nova-sprint \
  --state /path/to/untracked/sprint.twin -- init \
  --readers reader-m2 --members m1:1,m2:1
python3 orchestration/nova/twin.py --binary /path/to/nova-sprint \
  --state /path/to/untracked/sprint.twin -- where --json
```

The wrapper forces an explicit `mem:` state path, inherits only a minimal OS
environment, and refuses connection/credential overrides (including single-dash
Go flag forms) and commands such as `run`, `land` and fleet/session setup.
It must not be used as a live fleet
adapter. Read upstream `docs/FIRST-LAP.md` and installed command help for native
cards, dependencies, worker reports, review, holds and recovery. The production
`run` loop, not this wrapper, owns unattended transitions in a live deployment.

## Retire rules by purpose

The following is a migration assessment, not a change to any active harness
rule. Adopting these local tools does not activate that migration.

| Existing mechanism | Adoption decision |
|---|---|
| Chats remembering assignments and asking John to relay them | Replace with durable Nova cards and explicit next-owner state once live delivery is demonstrated. |
| Repeated acknowledgement/reminder prompts as the primary scheduler | Retire as scheduling controls; keep a concise human-facing explanation. |
| Copied allow-lists and protocol fingerprints | Consolidate where possible; an integration must still distinguish deployed from merely merged code. |
| One route per packet and every failure counted identically | Evaluate against real cost and attempt semantics; Nova capability tiers, effort and task routes are different axes. Do not silently change a spent ledger. |
| Budget, privacy and exact-head release checks | Keep the concrete protection while removing redundant ceremony; propose a precise change when a control obstructs useful work. |
| “Configured” or “message sent” reported as “running” or “done” | Replace with observed worker execution and accepted result evidence. |

## Live boundary and next integration step

Nova's live deployment needs the server, sprint Redis, separate bus Redis,
PostgreSQL configuration and companion Nova Tools worker/hook adapters.
This checkout does not provision those services or have a verified adapter
that can resume the managed ChatGPT/Claude remote sessions. A source review
is not proof that their supported CLI adapters can reach those sessions.

Next: demonstrate one real worker and reviewer through a supported delivery
adapter, including a lost delivery or interrupted worker, before transferring
the active PR13 queue. Preserve in-flight attempts and source IDs in migration;
do not replay approvals. Account for late Nova reports without manufacturing
a successful terminal receipt for an expired controlled packet. No additional
model call, account purchase or public release is started by these local commands.

## Evidence boundaries

The proof includes SHA-256 hashes of its producing script, local wrapper,
bootstrap, upstream lock and built binary. Recompute them after any change.
The smoke run actually tests refusal to merge before review and refusal to
overwrite an explicitly failed finish. Upstream's special deadline-failed
late-result recovery is a different source-reviewed path and is not exercised
by that negative test. This local profile has no controlled-packet adapter and
cannot regenerate any such packet's receipt.

The Go minimum intentionally rejects pre-releases below Go 1.26.6. An explicitly
inherited `GOPROXY` is honoured; direct VCS is the default only when unset.
The bootstrap checks the built engine's reported source commit before use.
Both simulation entry points run Nova in a scratch working directory with
an isolated HOME; the binary never runs in the checkout during the simulation.
Any file-path arguments to `twin.py` must be absolute because its working
directory is disposable. The explicit state path remains persistent.

Run the wrapper isolation tests with:
`python3 -B -m unittest discover -s orchestration/nova -p 'test_*.py'`.
