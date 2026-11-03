#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "fluent_fluent_bit__11556__acad02a", "activated_workflows": [".github/workflows/commit-lint.yaml", ".github/workflows/pr-commit-message.yaml", ".github/workflows/pr-integration-test.yaml", ".github/workflows/pr-lint.yaml", ".github/workflows/pr-package-tests.yaml", ".github/workflows/unit-tests.yaml"]}
EOF
