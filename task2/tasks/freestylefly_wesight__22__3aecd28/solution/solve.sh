#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "freestylefly_wesight__22__3aecd28", "activated_workflows": [".github/workflows/ci.yml", ".github/workflows/electron-verify.yml", ".github/workflows/labeler.yml", ".github/workflows/security.yml"]}
EOF
