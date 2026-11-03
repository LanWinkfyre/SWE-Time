#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "NVIDIA_NemoClaw__11417__3ea2d5f", "activated_workflows": [".github/workflows/code-scanning.yaml", ".github/workflows/codebase-growth-guardrails.yaml", ".github/workflows/commit-lint.yaml", ".github/workflows/dco-check.yaml", ".github/workflows/docs-cli-parity-pr.yaml", ".github/workflows/installer-hash-check.yaml", ".github/workflows/openshell-sdk-package-pr.yaml", ".github/workflows/pr.yaml", ".github/workflows/require-maintainer-edits.yaml"]}
EOF
