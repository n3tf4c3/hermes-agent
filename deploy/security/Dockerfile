# Security layer over the official v0.22.5 image; application source stays at the release.
# Rebuilds the Python environment from this fork's lock (brotlicffi 1.2.1.0, pyasn1 0.6.5,
# tornado 6.6) and the Photon sidecar's node_modules (undici 7.30.1, zod 4.6.7).
# Retire it when an official stable release ships these versions.
#
# Build from the repository root, on the host that runs it (arm64 on the server):
#   docker build -f deploy/security/Dockerfile -t hermes-agent:0.22.5-security-20261031 .
FROM nousresearch/hermes-agent:v0.22.5@sha256:9c5561579f3ffdf333401797094ac3a743738d6c25d40f4331c7bf77b694238d

LABEL org.opencontainers.image.version="0.22.5-security.20261031" \
      org.opencontainers.image.base.name="nousresearch/hermes-agent:v0.22.5" \
      org.opencontainers.image.base.digest="sha256:9c5561579f3ffdf333401797094ac3a743738d6c25d40f4331c7bf77b694238d"

COPY pyproject.toml uv.lock /opt/hermes/
COPY deploy/security/rebuild_env.py /tmp/hermes-security-rebuild.py
RUN /usr/local/bin/python3 /tmp/hermes-security-rebuild.py && rm /tmp/hermes-security-rebuild.py

# Same install as the official image: the sidecar's postinstall patch runs.
COPY plugins/platforms/photon/sidecar/package.json plugins/platforms/photon/sidecar/package-lock.json \
     /opt/hermes/plugins/platforms/photon/sidecar/
RUN cd /opt/hermes/plugins/platforms/photon/sidecar && \
    rm -rf node_modules && \
    npm ci --no-audit --fetch-retries=5 && \
    npm cache clean --force
