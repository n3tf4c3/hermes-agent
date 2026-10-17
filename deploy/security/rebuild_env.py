"""Rebuild the immutable image's dependency environment with the upstream PM path."""

from pathlib import Path
import shutil
import subprocess


root = Path("/opt/hermes").resolve()
venv = root / ".venv"
if venv.is_symlink() or venv.resolve().parent != root:
    raise RuntimeError("Refusing an environment outside the image's install tree")
shutil.rmtree(venv)

subprocess.run(
    [
        "/usr/local/bin/python3",
        "-m",
        "pm.build_env",
        "--source",
        str(root),
        "--python",
        "/usr/local/bin/python3",
        "--cache",
        str(root / "uv-cache"),
        "--out",
        str(venv),
        "--no-install-project",
        "--sealed",
        "--record-selection",
        "--extra",
        "all",
        "--extra",
        "messaging",
        "--extra",
        "otlp",
        "--extra",
        "anthropic",
        "--extra",
        "bedrock",
        "--extra",
        "azure-identity",
        "--extra",
        "matrix",
        "--extra",
        "google-chat",
    ],
    cwd=root,
    check=True,
    timeout=1800,
)
# Restore source binding and the console launchers used by the s6 services.
subprocess.run(
    [str(venv / "bin" / "python"), "-m", "docker.build_agent"],
    cwd=root,
    check=True,
    timeout=300,
)
# Shared package facts are non-secret image metadata, as in the upstream Dockerfile.
(root / "tools" / "facts.json").chmod(0o644)
(venv / ".lock").unlink(missing_ok=True)
