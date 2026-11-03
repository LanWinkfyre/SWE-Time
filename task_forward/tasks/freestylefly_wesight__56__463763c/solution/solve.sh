#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "freestylefly_wesight__56__463763c", "activated_workflows": [".github/workflows/ci.yml", ".github/workflows/electron-verify.yml", ".github/workflows/labeler.yml", ".github/workflows/security.yml"]}
EOF
