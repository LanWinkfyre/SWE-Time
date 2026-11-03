#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "cabinpkg_cabin__1237__427504d", "activated_workflows": [".github/workflows/ci.yml", ".github/workflows/codeql.yml", ".github/workflows/cpp.yml", ".github/workflows/docker.yml", ".github/workflows/docs.yml"]}
EOF
