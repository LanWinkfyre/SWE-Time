#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "pytorch_vision__8847__8bed9d8", "activated_workflows": [".github/workflows/build-cmake.yml", ".github/workflows/build-wheels-aarch64-linux.yml", ".github/workflows/build-wheels-linux.yml", ".github/workflows/build-wheels-m1.yml", ".github/workflows/build-wheels-windows.yml", ".github/workflows/docs.yml", ".github/workflows/lint.yml", ".github/workflows/prototype-tests-linux-gpu.yml", ".github/workflows/tests.yml"]}
EOF
