#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "hashicorp_consul__22574__59631ff", "activated_workflows": [".github/workflows/backport-checker.yml", ".github/workflows/bot-auto-approve.yaml", ".github/workflows/build-distros.yml", ".github/workflows/changelog-checker.yml", ".github/workflows/embedded-asset-checker.yml", ".github/workflows/go-tests.yml", ".github/workflows/goldenfile-checker.yml", ".github/workflows/pr-metrics-test-checker.yml", ".github/workflows/security-scan.yml", ".github/workflows/test-integrations.yml", ".github/workflows/verify-ci.yml"]}
EOF
