import json
import subprocess
import sys
from packaging.version import InvalidVersion, Version

repo, requested = sys.argv[1:]


def git(*args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


if requested in ("", "latest"):
    result = git("tag", "--merged", "origin/main")
    result.check_returncode()
    versions = []
    for tag in result.stdout.splitlines():
        try:
            versions.append((Version(tag.removeprefix("v")), tag))
        except InvalidVersion:
            continue
    if not versions:
        raise SystemExit("No release tag is reachable from origin/main")
    candidates = [max(versions)[1]]
else:
    candidates = (
        ["origin/main"] if requested == "main" else [requested, "v" + requested]
    )
for candidate in candidates:
    result = git("rev-parse", "--verify", "--end-of-options", candidate + "^{commit}")
    if result.returncode == 0:
        print(
            json.dumps(
                {"requested": requested, "ref": candidate, "sha": result.stdout.strip()}
            )
        )
        break
else:
    raise SystemExit("Unknown requested runtime revision: " + requested)
