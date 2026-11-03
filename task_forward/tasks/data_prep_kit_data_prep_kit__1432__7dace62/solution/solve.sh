#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "data_prep_kit_data_prep_kit__1432__7dace62", "activated_workflows": [".github/workflows/test-misc.yml", ".github/workflows/test-universal-tokenization-kfp.yml", ".github/workflows/test-universal-tokenization.yml", ".github/workflows/test-universal-tokenization2arrow.yml"]}
EOF
