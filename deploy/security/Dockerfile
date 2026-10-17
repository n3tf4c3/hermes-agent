# ARM64 deployment image; application source stays at the official 0.22.1 release.
FROM nousresearch/hermes-agent:v0.22.1@sha256:f24de2fd617c0bef83a8fcec4cda996aaa463705f8097e62ec4fb60eb2618d6b

LABEL org.opencontainers.image.version="0.22.1-security.20261015" \
      org.opencontainers.image.base.digest="sha256:f24de2fd617c0bef83a8fcec4cda996aaa463705f8097e62ec4fb60eb2618d6b"

COPY pyproject.toml uv.lock /opt/hermes/
COPY deploy/security/rebuild_env.py /tmp/hermes-security-rebuild.py
RUN /usr/local/bin/python3 /tmp/hermes-security-rebuild.py
