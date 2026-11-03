#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "ogx_ai_ogx__6452__f73a00f", "activated_workflows": [".github/workflows/ci-status.yml", ".github/workflows/codeql.yml", ".github/workflows/pre-commit.yml", ".github/workflows/pypi.yml", ".github/workflows/semantic-pr.yml", ".github/workflows/trivy-security.yml", ".github/workflows/ui-unit-tests.yml"]}
EOF
