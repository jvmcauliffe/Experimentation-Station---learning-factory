### Base commit

84075ef1114ba27d927074a8f6255cb1c39fc6c5

### Outcome

One pull request, left unmerged, that lets a harness-hosted report-only review packet name jvmcauliffe/Experimentation-Station---learning-factory as its Review input repository, so Codex can review the HN goldmine handover (PR 2 there, commit bd2863d) through the normal packet route. No other repository acquires any new role.

### Task items

1. In scripts/validate_openai_task.py add a separate REVIEW_REPOSITORIES set equal to REPOSITORIES plus jvmcauliffe/Experimentation-Station---learning-factory, written in the same case convention the existing entries and comparisons use. Use it only in the Review input repository check (the "Unauthorised review repository" requirement). Leave REPOSITORIES and every other use of it (Target repository, writer repository) unchanged.
2. In scripts/openai_report_packet.py take the --review-repository choices from REVIEW_REPOSITORIES instead of REPOSITORIES.
3. Add tests: a report-only packet with the new review repository lints clean; the same repository as Target repository is still refused; a docs/private path is still refused; an unlisted repository is still refused. Update any existing test that asserts the old choices.
4. Run the full unit test suite as one standalone command and report the last lines.

### In-scope paths

scripts/validate_openai_task.py
scripts/openai_report_packet.py
tests/test_openai_task.py
tests/test_openai_report_packet.py

### Out-of-scope

REPOSITORIES semantics, Target repository and writer checks, quotas, caps, claims, the admission adapter, the receiver, .github workflows, scripts/validate_claude_task.py, any docs, and any other file. No merge, publish or trigger comment. Do not read or copy anything from the Experimentation-Station repository.

### Authority

implement-and-open-pr

### Model route

standard_reasoning

### Effort level

low

### Acceptance checks

python3 -m unittest discover -s tests passes in full, run as a single standalone command. The diff touches only the four in-scope paths. REPOSITORIES is byte-for-byte unchanged. The new tests fail on the old code and pass on the new.

### Evidence packet

This issue body, plus scripts/validate_openai_task.py lines 15 to 120, scripts/openai_report_packet.py, and the two named test files at the base commit.

### Reusable review receipts

None

### Maximum turns

8

### Correction retries

0

### Run budget (USD)

0.50

### Work units

2

### Expected duration (minutes)

8

### Maximum delegated model calls

0

### Requested parallel workers

1

### Stop conditions

Stop if the change would need an edit outside the four in-scope paths, if it would widen the Target repository or writer allow-lists, if the base commit is stale, if any test outside the new ones fails for an unrelated reason, or on any ambiguity about the case convention. Report the exact failed operation and do not retry.

### Handover destination

This issue and the pull request. Open one draft pull request and leave it unmerged for independent review. Record in the report that whether the Codex connector can read the Experimentation-Station repository is unverified.
