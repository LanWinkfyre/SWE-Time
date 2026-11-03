#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "ogx_ai_ogx__4817__7a7b248", "activated_workflows": [".github/workflows/ci-status.yml", ".github/workflows/integration-auth-tests.yml", ".github/workflows/integration-responses-conversations-auth-tests.yml", ".github/workflows/integration-tests.yml", ".github/workflows/pre-commit.yml", ".github/workflows/pypi.yml", ".github/workflows/semantic-pr.yml", ".github/workflows/test-external-provider-module.yml", ".github/workflows/test-external.yml"]}
EOF
