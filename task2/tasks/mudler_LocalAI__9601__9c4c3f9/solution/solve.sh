#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "mudler_LocalAI__9601__9c4c3f9", "activated_workflows": [".github/workflows/backend_pr.yml", ".github/workflows/build-test.yaml", ".github/workflows/image-pr.yml", ".github/workflows/lint.yml", ".github/workflows/test-extra.yml", ".github/workflows/yaml-check.yml"]}
EOF
