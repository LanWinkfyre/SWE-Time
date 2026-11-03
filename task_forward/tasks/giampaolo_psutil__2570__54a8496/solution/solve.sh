#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "giampaolo_psutil__2570__54a8496", "activated_workflows": [".github/workflows/bsd.yml", ".github/workflows/build.yml", ".github/workflows/issues.yml"]}
EOF
