#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "microsoft_waza__448__a431744", "activated_workflows": [".github/workflows/auto-merge.yml", ".github/workflows/docker-ci.yml", ".github/workflows/go-ci.yml", ".github/workflows/squad-ci.yml"]}
EOF
