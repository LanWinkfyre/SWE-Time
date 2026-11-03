#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "ogx_ai_ogx__4821__2554a9e", "activated_workflows": [".github/workflows/pre-commit.yml", ".github/workflows/pypi.yml", ".github/workflows/semantic-pr.yml"]}
EOF
