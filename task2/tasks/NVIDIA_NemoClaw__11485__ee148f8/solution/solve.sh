#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "NVIDIA_NemoClaw__11485__ee148f8", "activated_workflows": [".github/workflows/code-scanning.yaml", ".github/workflows/codebase-growth-guardrails.yaml", ".github/workflows/commit-lint.yaml", ".github/workflows/dco-check.yaml", ".github/workflows/docs-links-pr.yaml", ".github/workflows/installer-hash-check.yaml", ".github/workflows/pr.yaml", ".github/workflows/require-maintainer-edits.yaml"]}
EOF
