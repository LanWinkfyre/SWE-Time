#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "ZSWatch_ZSWatch__423__5f4a45b", "activated_workflows": [".github/workflows/ci.yml"]}
EOF
