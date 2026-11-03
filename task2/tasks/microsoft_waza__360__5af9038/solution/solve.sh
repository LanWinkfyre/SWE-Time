#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "microsoft_waza__360__5af9038", "activated_workflows": [".github/workflows/auto-merge.yml", ".github/workflows/docker-ci.yml", ".github/workflows/go-ci.yml", ".github/workflows/squad-ci.yml", ".github/workflows/waza-eval.yml"]}
EOF
