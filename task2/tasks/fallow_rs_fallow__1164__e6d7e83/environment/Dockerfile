# Pre-change working tree of fallow-rs/fallow at e6d7e8316474e27dcd4ba3f616c5ca494b8df92a, no git history.
# rebuild/rebuild.py places the tree in ./repo next to this file, so the build context is this
# environment/ directory (harbor's default).  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN python3 /opt/swe-time/tree_digest.py --repo /testbed/repo --stage baseline \
        --out /opt/swe-time/receipt.json
