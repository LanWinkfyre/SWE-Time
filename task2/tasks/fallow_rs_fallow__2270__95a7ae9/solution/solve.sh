#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "fallow_rs_fallow__2270__95a7ae9", "activated_workflows": [".github/workflows/allocs.yml", ".github/workflows/bench-type-aware.yml", ".github/workflows/bench.yml", ".github/workflows/bloat.yml", ".github/workflows/ci.yml", ".github/workflows/commitlint.yml", ".github/workflows/coupling.yml", ".github/workflows/coverage.yml", ".github/workflows/cross-arch.yml", ".github/workflows/dependabot-auto-merge.yml", ".github/workflows/ecosystem.yml", ".github/workflows/fuzz-smoke.yml"]}
EOF
