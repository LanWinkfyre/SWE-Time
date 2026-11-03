#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "ogx_ai_ogx__6116__229c260", "activated_workflows": [".github/workflows/ci-status.yml", ".github/workflows/codeql.yml", ".github/workflows/integration-auth-tests.yml", ".github/workflows/integration-responses-conversations-auth-tests.yml", ".github/workflows/integration-tests.yml", ".github/workflows/integration-vector-io-tests.yml", ".github/workflows/pre-commit.yml", ".github/workflows/pypi.yml", ".github/workflows/record-integration-tests.yml", ".github/workflows/semantic-pr.yml", ".github/workflows/test-external.yml", ".github/workflows/unit-tests.yml"]}
EOF
