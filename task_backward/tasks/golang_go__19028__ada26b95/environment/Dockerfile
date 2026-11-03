# golang/go cut at aa1538799601bdbc881f2ad3133184377b7e7aca: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e7ec06e000627ad699a274a5a672bc3f63d6a709 \
        --stage baseline --out /opt/swe-time/receipt.json
