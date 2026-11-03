#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "giampaolo_psutil__2695__35529fa", "activated_workflows": [".github/workflows/build.yml", ".github/workflows/docs.yml"]}
EOF
