"""Swap release source files for this fork's fixed copies, only over the exact release bytes."""

from hashlib import sha256
from pathlib import Path
import shutil


root = Path("/opt/hermes").resolve()
staged = Path("/tmp/hermes-security-sources").resolve()

# Release file -> (sha256 in v0.22.5, sha256 of the fixed copy).
FIXES = {
    # Audit finding #7: cookie writes from same-site siblings (fork commit 64416f43b8).
    "hermes_cli/dashboard_auth/middleware.py": (
        "4036350adce2e6711dba2a1448abe94450f80b8275df82f9acad4257c4add2cf",
        "922cc8bdbe987e9b926ee6ec1750e764de9121133ad94ad09ca77f50c7d030ad",
    ),
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


for rel, (release_sha, fixed_sha) in FIXES.items():
    target = root / rel
    source = staged / rel
    if digest(target) != release_sha:
        raise RuntimeError(f"{rel} is not the v0.22.5 file; rebase the fix before building")
    if digest(source) != fixed_sha:
        raise RuntimeError(f"{rel}: staged copy is not the reviewed fix")
    shutil.copyfile(source, target)
    for cached in target.parent.glob(f"__pycache__/{target.stem}.*.pyc"):
        cached.unlink()
    print(f"fixed {rel}")
