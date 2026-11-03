# Pre-change working tree of mudler/LocalAI at 2b1f6d27e95cd70d58de73eaa9bc6209380adec5, no git history.
# rebuild/rebuild.py places the tree in ./repo next to this file, so the build context is this
# environment/ directory (harbor's default).  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN python3 /opt/swe-time/tree_digest.py --repo /testbed/repo --stage baseline \
        --out /opt/swe-time/receipt.json
