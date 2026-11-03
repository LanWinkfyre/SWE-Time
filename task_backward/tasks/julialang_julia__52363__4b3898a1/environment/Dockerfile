# JuliaLang/julia cut at aef528d32a6291ce82452c3a1ff1fa56ccf17641: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 641f717a15cf89964db446c1bb32d0d672763786 \
        --stage baseline --out /opt/swe-time/receipt.json
