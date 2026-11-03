# Pre-change working tree of fallow-rs/fallow at e207ccdcdd2f44b18d28030ef791e70ac5b1588c, no git history.
# rebuild/rebuild.py places the tree in ./repo next to this file, so the build context is this
# environment/ directory (harbor's default).  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN python3 /opt/swe-time/tree_digest.py --repo /testbed/repo --stage baseline \
        --out /opt/swe-time/receipt.json
