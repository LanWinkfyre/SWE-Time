#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "giampaolo_psutil__2611__5fcc850", "activated_workflows": [".github/workflows/bsd.yml", ".github/workflows/docs.yml", ".github/workflows/sunos.yml", ".github/workflows/tests.yml", ".github/workflows/wheels.yml"]}
EOF
