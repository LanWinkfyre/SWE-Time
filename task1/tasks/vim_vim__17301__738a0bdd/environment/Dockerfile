# vim/vim cut at 73440245361f3399b88c872236830da3086ad942: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d4110e06952be7d06ba39cf0434626bbd7301a9d \
        --stage baseline --out /opt/swe-time/receipt.json
