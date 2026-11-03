#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "mudler_LocalAI__10806__cdb6702", "activated_workflows": [".github/workflows/backend_pr.yml", ".github/workflows/build-test.yaml", ".github/workflows/image-pr.yml", ".github/workflows/lint.yml", ".github/workflows/test-extra.yml", ".github/workflows/test.yml", ".github/workflows/tests-e2e.yml", ".github/workflows/tests-ui-e2e.yml", ".github/workflows/yaml-check.yml"]}
EOF
