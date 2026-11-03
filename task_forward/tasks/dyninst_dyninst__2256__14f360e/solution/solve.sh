#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "dyninst_dyninst__2256__14f360e", "activated_workflows": [".github/workflows/binary-tests.yaml", ".github/workflows/codegen-cross-build.yaml", ".github/workflows/libabigail.yaml", ".github/workflows/pr-tests.yaml"]}
EOF
