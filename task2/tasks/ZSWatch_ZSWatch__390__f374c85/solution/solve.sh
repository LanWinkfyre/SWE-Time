#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "ZSWatch_ZSWatch__390__f374c85", "activated_workflows": [".github/workflows/ci.yml"]}
EOF
