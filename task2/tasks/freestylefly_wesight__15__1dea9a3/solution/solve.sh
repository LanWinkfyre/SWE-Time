#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "freestylefly_wesight__15__1dea9a3", "activated_workflows": [".github/workflows/ci.yml", ".github/workflows/electron-verify.yml", ".github/workflows/labeler.yml", ".github/workflows/openclaw-check.yml", ".github/workflows/security.yml"]}
EOF
