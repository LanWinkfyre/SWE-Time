#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "pytorch_rl__3288__c43f212", "activated_workflows": [".github/workflows/benchmarks.yml", ".github/workflows/benchmarks_pr.yml", ".github/workflows/build-wheels-aarch64-linux.yml", ".github/workflows/build-wheels-linux.yml", ".github/workflows/build-wheels-m1.yml", ".github/workflows/build-wheels-windows.yml", ".github/workflows/docs.yml", ".github/workflows/lint.yml", ".github/workflows/nightly_build.yml", ".github/workflows/test-linux-habitat.yml", ".github/workflows/test-linux-libs.yml", ".github/workflows/test-linux-llm.yml", ".github/workflows/test-linux-sota.yml", ".github/workflows/test-linux.yml", ".github/workflows/test-windows-optdepts.yml"]}
EOF
