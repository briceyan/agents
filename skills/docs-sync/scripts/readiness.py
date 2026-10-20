import json
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
manifest = json.loads(path.read_text())
required = (
    "docs typecheck",
    "cli generator suite",
    "api generator suite",
    "production build",
    "site and syntax browser tests",
    "dev navigation browser tests",
    "whitespace check",
    "internal link targets",
    "fragment and anchor targets",
    "copied source links",
    "navigation registration",
    "copy fidelity",
    "regeneration reproducibility",
    "cli reference coverage",
    "api reference totals",
    "public example parse",
    "diff scope",
    "originals untouched",
)
verification = manifest.setdefault("verification", {})
checks = {check["name"]: check for check in verification.get("checks", [])}
failures = []
for name in required:
    check = checks.get(name, {})
    accepted = (0, 1) if name == "copy fidelity" else (0,)
    if (
        check.get("status") not in ("pass", "passed")
        or check.get("exit_code") not in accepted
    ):
        failures.append(name)
if manifest.get("blockers"):
    failures.append("recorded blockers")
status = "blocked" if failures else "ready"
manifest["status"] = verification["status"] = status
manifest["readiness_gate"] = {"required": list(required), "failures": failures}
path.write_text(json.dumps(manifest, indent=2) + "\n")
report = path.with_name("report.md")
text = (
    report.read_text()
    if report.exists()
    else "# Docs refresh\n\n- **Status:** pending\n"
)
text = re.sub(r"(?m)^- \*\*Status:\*\*.*$", "- **Status:** " + status, text)
text = text.split("\n## Readiness gate\n", 1)[0]
detail = ", ".join(failures) if failures else "all required checks passed"
report.write_text(
    text + "\n## Readiness gate\n\nComputed status: " + status + ". " + detail + ".\n"
)
print(json.dumps({"status": status, "failures": failures, "report": str(report)}))
raise SystemExit(1 if failures else 0)
