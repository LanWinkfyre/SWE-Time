#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "data_prep_kit_data_prep_kit__1100__9db7e98", "activated_workflows": [".github/workflows/build-library.yml", ".github/workflows/test.yml"]}
EOF
