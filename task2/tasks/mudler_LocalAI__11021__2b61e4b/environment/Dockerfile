# Pre-change working tree of mudler/LocalAI at 2b61e4bc1d84f4fad786ae024f74e12f059b7389, no git history.
# rebuild/rebuild.py places the tree in ./repo next to this file, so the build context is this
# environment/ directory (harbor's default).  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN python3 /opt/swe-time/tree_digest.py --repo /testbed/repo --stage baseline \
        --out /opt/swe-time/receipt.json
