#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "mudler_LocalAI__10062__11403f4", "activated_workflows": [".github/workflows/backend_pr.yml", ".github/workflows/test-extra.yml", ".github/workflows/test.yml", ".github/workflows/yaml-check.yml"]}
EOF
