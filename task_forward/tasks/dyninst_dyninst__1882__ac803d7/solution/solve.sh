#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "dyninst_dyninst__1882__ac803d7", "activated_workflows": [".github/workflows/libabigail.yaml", ".github/workflows/pr-tests.yaml"]}
EOF
