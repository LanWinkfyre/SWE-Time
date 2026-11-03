#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "emmercm_igir__2411__a714680", "activated_workflows": [".github/workflows/codecov.yml", ".github/workflows/gh-dependabot-automerge.yml", ".github/workflows/gh-label-sync.yml", ".github/workflows/gh-pages.yml", ".github/workflows/lint.yml", ".github/workflows/node-compile.yml", ".github/workflows/node-dependency-watchdog.yml", ".github/workflows/node-test-package.yml", ".github/workflows/node-test.yml", ".github/workflows/pr-renamer.yml", ".github/workflows/scoop-test.yml"]}
EOF
